$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$testRoot = Join-Path $projectRoot '.mobile-test'
$previous = @{}
foreach ($name in @('PLAYWRIGHT_BROWSERS_PATH', 'npm_config_cache', 'TEMP', 'TMP')) {
    $previous[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

try {
    New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
    $env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $testRoot 'browsers'
    $env:npm_config_cache = Join-Path $testRoot 'npm-cache'
    $env:TEMP = Join-Path $testRoot 'tmp'
    $env:TMP = $env:TEMP
    New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null

    & npm.cmd install --prefix $testRoot --no-save --no-package-lock playwright@1.64.1
    if ($LASTEXITCODE -ne 0) { throw 'Playwright installation failed.' }
    & node (Join-Path $testRoot 'node_modules\playwright\cli.js') install chromium --only-shell
    if ($LASTEXITCODE -ne 0) { throw 'Chromium installation failed.' }
    Write-Host 'Local browser test tools are ready.'
} finally {
    foreach ($name in $previous.Keys) {
        [Environment]::SetEnvironmentVariable($name, $previous[$name], 'Process')
    }
}
