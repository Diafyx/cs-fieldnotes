param(
    [switch]$UseCurrentVersion,
    [ValidatePattern('^[0-9]+\.[0-9]+\.[0-9]+$')]
    [string]$VersionName,
    [switch]$CheckOnly,
    [switch]$ArchiveExisting
)

$ErrorActionPreference = 'Stop'
if ($UseCurrentVersion -eq [bool]$VersionName) {
    throw 'Choose either -UseCurrentVersion or -VersionName x.y.z.'
}
if ($ArchiveExisting -and (!$UseCurrentVersion -or $CheckOnly)) {
    throw '-ArchiveExisting needs -UseCurrentVersion and cannot be combined with -CheckOnly.'
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$gradleFile = Join-Path $projectRoot 'android\app\build.gradle'
$original = [IO.File]::ReadAllText($gradleFile)
$codeMatches = [regex]::Matches($original, '(?m)^[ \t]*versionCode ([0-9]+)[ \t]*$')
$nameMatches = [regex]::Matches($original, "(?m)^[ \t]*versionName '([0-9]+\.[0-9]+\.[0-9]+)'[ \t]*$")
if ($codeMatches.Count -ne 1 -or $nameMatches.Count -ne 1) {
    throw 'Could not read one versionCode and versionName from android/app/build.gradle.'
}

$currentCode = [int]$codeMatches[0].Groups[1].Value
$currentName = $nameMatches[0].Groups[1].Value
if ($UseCurrentVersion) {
    $releaseCode = $currentCode
    $releaseName = $currentName
} else {
    if ([version]$VersionName -le [version]$currentName) {
        throw "The new version name must be higher than $currentName."
    }
    if ($currentCode -eq [int]::MaxValue) { throw 'There is no room for another version code.' }
    $releaseCode = $currentCode + 1
    $releaseName = $VersionName
}

$notesFile = Join-Path $projectRoot "play-store\release-notes\$releaseCode.txt"
if (!(Test-Path -LiteralPath $notesFile -PathType Leaf)) {
    throw "Write the Play release notes first: $notesFile"
}
$notes = [IO.File]::ReadAllText($notesFile).Trim()
if ([string]::IsNullOrWhiteSpace($notes) -or $notes.Length -gt 500) {
    throw 'Release notes must contain 1 to 500 characters.'
}

$archive = Join-Path $projectRoot ".android-tools\play-releases\$releaseCode-$releaseName"
if (!$CheckOnly -and (Test-Path -LiteralPath $archive)) {
    throw "This release already has an archive: $archive"
}

$apk = Join-Path $projectRoot 'android\app\build\outputs\apk\release\app-release.apk'
$bundle = Join-Path $projectRoot 'android\app\build\outputs\bundle\release\app-release.aab'
$aapt = Join-Path $projectRoot '.android-tools\android-sdk\build-tools\36.0.0\aapt.exe'
$apksignerJar = Join-Path $projectRoot '.android-tools\android-sdk\build-tools\36.0.0\lib\apksigner.jar'
$jdk = Get-ChildItem -LiteralPath (Join-Path $projectRoot '.android-tools\jdk17') -Directory | Select-Object -First 1
if ($null -eq $jdk) { throw 'The local JDK 17 is missing.' }
$java = Join-Path $jdk.FullName 'bin\java.exe'
if (!(Test-Path -LiteralPath $aapt -PathType Leaf) -or !(Test-Path -LiteralPath $apksignerJar -PathType Leaf) `
        -or !(Test-Path -LiteralPath $java -PathType Leaf)) {
    throw 'The local Android build tools are missing.'
}

$updated = $false
try {
    & python (Join-Path $projectRoot 'scripts\prepare_android.py')
    if ($LASTEXITCODE -ne 0) { throw 'Preparing the Android pages failed.' }
    & python (Join-Path $projectRoot 'scripts\check_android.py')
    if ($LASTEXITCODE -ne 0) { throw 'The Android page check failed.' }
    & python (Join-Path $projectRoot 'scripts\check_play_store.py')
    if ($LASTEXITCODE -ne 0) { throw 'The Play listing file check failed.' }
    if ($CheckOnly) {
        Write-Host "Checks passed for version $releaseName ($releaseCode). No release was built."
        return
    }

    if (!$UseCurrentVersion) {
        $changed = $original.Replace($codeMatches[0].Value,
            $codeMatches[0].Value.Replace("versionCode $currentCode", "versionCode $releaseCode"))
        $changed = $changed.Replace($nameMatches[0].Value,
            $nameMatches[0].Value.Replace("'$currentName'", "'$releaseName'"))
        [IO.File]::WriteAllText($gradleFile, $changed)
        $updated = $true
    }

    if (!$ArchiveExisting) {
        & (Join-Path $projectRoot 'scripts\release_android.ps1')
    } else {
        Write-Host 'Checking the existing signed release files before archiving.'
    }
    if (!(Test-Path -LiteralPath $apk -PathType Leaf) -or !(Test-Path -LiteralPath $bundle -PathType Leaf)) {
        throw 'The release APK or Play bundle is missing.'
    }

    $badging = & $aapt dump badging $apk
    $aaptExitCode = $LASTEXITCODE
    if ($aaptExitCode -ne 0) { throw "Could not read the built APK metadata (aapt exit code $aaptExitCode)." }
    $packageLine = ($badging | Select-String '^package:' | Select-Object -First 1).Line
    if ($packageLine -notmatch "name='org\.diafyx\.fieldnotes' versionCode='$releaseCode' versionName='$([regex]::Escape($releaseName))'") {
        throw "The built APK has the wrong package or version. Expected org.diafyx.fieldnotes $releaseName ($releaseCode). Found: $packageLine"
    }

    $signature = & $java -jar $apksignerJar verify --print-certs $apk
    if ($LASTEXITCODE -ne 0) { throw 'The APK signature check failed.' }
    $fingerprint = [regex]::Match(($signature -join "`n"), 'Signer #1 certificate SHA-256 digest: ([0-9a-fA-F]{64})').Groups[1].Value.ToLowerInvariant()
    $expectedFingerprint = '2072ef88ab6be2055dd154366e5458c0a3647a511b10ac7aca8d1ff5ff14df28'
    if ($fingerprint -ne $expectedFingerprint) {
        throw 'The APK was signed with a different key. Check the release keystore before uploading.'
    }

    & python (Join-Path $projectRoot 'scripts\check_play_store.py') --apk $apk --bundle $bundle --owner-key
    if ($LASTEXITCODE -ne 0) { throw 'The built Play release check failed.' }

    New-Item -ItemType Directory -Path $archive -Force | Out-Null
    Copy-Item -LiteralPath $apk -Destination (Join-Path $archive 'fieldnotes.apk')
    Copy-Item -LiteralPath $bundle -Destination (Join-Path $archive 'fieldnotes.aab')
    Copy-Item -LiteralPath $notesFile -Destination (Join-Path $archive 'release-notes.txt')
    $apkHash = (Get-FileHash -LiteralPath (Join-Path $archive 'fieldnotes.apk') -Algorithm SHA256).Hash
    $bundleHash = (Get-FileHash -LiteralPath (Join-Path $archive 'fieldnotes.aab') -Algorithm SHA256).Hash
    $record = @(
        'Fieldnotes Play release'
        "Package: org.diafyx.fieldnotes"
        "Version: $releaseName ($releaseCode)"
        "Built UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss'))"
        "APK SHA-256: $apkHash"
        "Bundle SHA-256: $bundleHash"
        "Upload key SHA-256: $fingerprint"
    ) -join "`r`n"
    [IO.File]::WriteAllText((Join-Path $archive 'release-info.txt'), $record + "`r`n")
    Write-Host "Play upload file: $(Join-Path $archive 'fieldnotes.aab')"
    Write-Host "Release notes: $(Join-Path $archive 'release-notes.txt')"
    Write-Host "Release details: $(Join-Path $archive 'release-info.txt')"
} catch {
    if ($updated) { [IO.File]::WriteAllText($gradleFile, $original) }
    throw
}
