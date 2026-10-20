param([switch]$CreateKey)

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$toolsRoot = Join-Path $projectRoot '.android-tools'
$signingDir = Join-Path $toolsRoot 'signing'
$keyFile = Join-Path $signingDir 'fieldnotes-release.jks'
$jdkDir = Join-Path $toolsRoot 'jdk17'
$jdk = Get-ChildItem -LiteralPath $jdkDir -Directory | Select-Object -First 1
if ($null -eq $jdk) { throw 'The local JDK 17 was not found in .android-tools/jdk17.' }

$ignored = Get-Content -LiteralPath (Join-Path $projectRoot '.gitignore')
if ($ignored -notcontains '.android-tools/') {
    throw '.android-tools/ must be ignored before creating a release key.'
}

$managedEnvironment = @('JAVA_HOME', 'GRADLE_USER_HOME', 'ANDROID_HOME', 'ANDROID_USER_HOME',
    'TEMP', 'TMP', 'JAVA_TOOL_OPTIONS', 'FIELDNOTES_KEYSTORE',
    'FIELDNOTES_KEYSTORE_PASSWORD', 'FIELDNOTES_KEY_ALIAS', 'FIELDNOTES_KEY_PASSWORD')
$previousEnvironment = @{}
foreach ($name in $managedEnvironment) {
    $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

try {
$env:JAVA_HOME = $jdk.FullName
$env:GRADLE_USER_HOME = Join-Path $toolsRoot 'gradle-cache'
$env:ANDROID_HOME = Join-Path $toolsRoot 'android-sdk'
$env:ANDROID_USER_HOME = Join-Path $toolsRoot 'android-user'
$env:TEMP = $toolsRoot
$env:TMP = $toolsRoot
$env:JAVA_TOOL_OPTIONS = '-Duser.home="' + (Join-Path $toolsRoot 'user-home') + '" -Djava.io.tmpdir="' + $toolsRoot + '"'

if ($CreateKey) {
    if (Test-Path -LiteralPath $keyFile) { throw 'The release key already exists. It was not changed.' }
    New-Item -ItemType Directory -Path $signingDir -Force | Out-Null
    $keytool = Join-Path $env:JAVA_HOME 'bin\keytool.exe'
    & $keytool -genkeypair -keystore $keyFile -storetype PKCS12 -alias fieldnotes `
        -keyalg RSA -keysize 3072 -validity 10000 -dname 'CN=Fieldnotes'
    if ($LASTEXITCODE -ne 0) { throw 'The release key was not created.' }
    Write-Host "Release key created: $keyFile"
    Write-Host 'Back up this key and its password before you share a release APK.'
    return
}

if (!(Test-Path -LiteralPath $keyFile -PathType Leaf)) {
    throw 'The release key is missing. Run this script with -CreateKey first.'
}

$secret = Read-Host 'Release key password' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
try {
    $password = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
}
if ([string]::IsNullOrEmpty($password)) { throw 'The release key password cannot be empty.' }

$env:FIELDNOTES_KEYSTORE = $keyFile
$env:FIELDNOTES_KEYSTORE_PASSWORD = $password
$env:FIELDNOTES_KEY_ALIAS = 'fieldnotes'
$env:FIELDNOTES_KEY_PASSWORD = $password
$gradle = Join-Path $toolsRoot 'gradle\gradle-9.6.0\bin\gradle.bat'
if (!(Test-Path -LiteralPath $gradle -PathType Leaf)) {
    throw 'The local Gradle 9.6.0 was not found in .android-tools/gradle.'
}

try {
    & $gradle :app:lintRelease :app:assembleRelease :app:bundleRelease --console=plain -p (Join-Path $projectRoot 'android')
    if ($LASTEXITCODE -ne 0) { throw 'The release build failed.' }

    $apk = Join-Path $projectRoot 'android\app\build\outputs\apk\release\app-release.apk'
    if (!(Test-Path -LiteralPath $apk -PathType Leaf)) { throw 'The release APK was not found.' }
    $buildTools = Join-Path $env:ANDROID_HOME 'build-tools\36.0.0'
    $aapt = Join-Path $buildTools 'aapt.exe'
    $apksigner = Join-Path $buildTools 'apksigner.bat'
    $permissions = & $aapt dump permissions $apk
    if ($LASTEXITCODE -ne 0) { throw 'The APK permission check failed.' }
    if ($permissions | Select-String '^uses-permission') { throw 'The release APK requests a permission.' }
    & $apksigner verify --verbose --print-certs $apk
    if ($LASTEXITCODE -ne 0) { throw 'The APK signature check failed.' }
    $bundle = Join-Path $projectRoot 'android\app\build\outputs\bundle\release\app-release.aab'
    if (!(Test-Path -LiteralPath $bundle -PathType Leaf)) { throw 'The Play Store bundle was not found.' }
    $jarsigner = Join-Path $env:JAVA_HOME 'bin\jarsigner.exe'
    $ErrorActionPreference = 'Continue'
    try {
        $bundleCheck = & $jarsigner -verify $bundle 2>&1
    } finally {
        $ErrorActionPreference = 'Stop'
    }
    if ($LASTEXITCODE -ne 0 -or !($bundleCheck -match 'jar verified')) {
        throw 'The Play Store bundle signature check failed.'
    }
    Write-Host "Release APK: $apk"
    Write-Host ('APK SHA-256: ' + (Get-FileHash -LiteralPath $apk -Algorithm SHA256).Hash)
    Write-Host "Play Store bundle: $bundle"
    Write-Host ('Bundle SHA-256: ' + (Get-FileHash -LiteralPath $bundle -Algorithm SHA256).Hash)
} finally {
    & $gradle --stop --console=plain -p (Join-Path $projectRoot 'android') | Out-Null
    $env:FIELDNOTES_KEYSTORE = $null
    $env:FIELDNOTES_KEYSTORE_PASSWORD = $null
    $env:FIELDNOTES_KEY_ALIAS = $null
    $env:FIELDNOTES_KEY_PASSWORD = $null
    $password = $null
    $secret.Dispose()
}
} finally {
    foreach ($name in $managedEnvironment) {
        [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], 'Process')
    }
}
