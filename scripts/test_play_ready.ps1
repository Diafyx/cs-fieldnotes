param(
    [switch]$Submission,
    [string]$SupportEmail
)

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$toolsRoot = Join-Path $projectRoot '.android-tools'
$jdk = Get-ChildItem -LiteralPath (Join-Path $toolsRoot 'jdk17') -Directory | Select-Object -First 1
if ($null -eq $jdk) { throw 'The local JDK 17 is missing.' }
$gradle = Join-Path $toolsRoot 'gradle\gradle-9.6.0\bin\gradle.bat'
if (!(Test-Path -LiteralPath $gradle -PathType Leaf)) { throw 'The local Gradle 9.6.0 is missing.' }

$managed = @('JAVA_HOME', 'GRADLE_USER_HOME', 'ANDROID_HOME', 'ANDROID_USER_HOME',
    'TEMP', 'TMP', 'JAVA_TOOL_OPTIONS')
$previous = @{}
foreach ($name in $managed) {
    $previous[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

try {
    $env:JAVA_HOME = $jdk.FullName
    $env:GRADLE_USER_HOME = Join-Path $toolsRoot 'gradle-cache'
    $env:ANDROID_HOME = Join-Path $toolsRoot 'android-sdk'
    $env:ANDROID_USER_HOME = Join-Path $toolsRoot 'android-user'
    $env:TEMP = $toolsRoot
    $env:TMP = $toolsRoot
    $env:JAVA_TOOL_OPTIONS = '-Duser.home="' + (Join-Path $toolsRoot 'user-home') + '" -Djava.io.tmpdir="' + $toolsRoot + '"'

    & python (Join-Path $projectRoot 'scripts\prepare_android.py')
    if ($LASTEXITCODE -ne 0) { throw 'Android page preparation failed.' }
    $checks = Get-ChildItem -LiteralPath (Join-Path $projectRoot 'scripts') -Filter 'check*.py' | Sort-Object Name
    foreach ($check in $checks) {
        & python $check.FullName
        if ($LASTEXITCODE -ne 0) { throw "Content check failed: $($check.Name)" }
    }

    & $gradle :app:lintDebug :app:assembleDebug :app:bundleDebug --console=plain -p (Join-Path $projectRoot 'android')
    if ($LASTEXITCODE -ne 0) { throw 'Android debug build or lint failed.' }
    $apk = Join-Path $projectRoot 'android\app\build\outputs\apk\debug\app-debug.apk'
    $bundle = Join-Path $projectRoot 'android\app\build\outputs\bundle\debug\app-debug.aab'
    & python (Join-Path $projectRoot 'scripts\check_play_store.py') --apk $apk --bundle $bundle
    if ($LASTEXITCODE -ne 0) { throw 'Built app check failed.' }

    $previousBrowsers = [Environment]::GetEnvironmentVariable('PLAYWRIGHT_BROWSERS_PATH', 'Process')
    try {
        $env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $projectRoot '.mobile-test\browsers'
        & node (Join-Path $projectRoot 'scripts\test_android_ui.js')
        if ($LASTEXITCODE -ne 0) { throw 'Android browser UI check failed.' }
    } finally {
        [Environment]::SetEnvironmentVariable('PLAYWRIGHT_BROWSERS_PATH', $previousBrowsers, 'Process')
    }

    if ($Submission) {
        & python (Join-Path $projectRoot 'scripts\check_play_store.py') --submission --support-email $SupportEmail --apk $apk --bundle $bundle
        if ($LASTEXITCODE -ne 0) { throw 'Play submission check failed.' }
    }
    Write-Host 'Local Play tests passed. The debug bundle is for testing only.'
} finally {
    & $gradle --stop --console=plain -p (Join-Path $projectRoot 'android') | Out-Null
    foreach ($name in $managed) {
        [Environment]::SetEnvironmentVariable($name, $previous[$name], 'Process')
    }
}
