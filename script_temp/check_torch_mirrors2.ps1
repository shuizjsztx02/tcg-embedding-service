$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'

function Probe($name, $url) {
    Write-Output ("=== " + $name + " ===")
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 60
        Write-Output ("status: " + $r.StatusCode + ", bytes: " + $r.RawContentLength)
        return $r.Content
    } catch {
        Write-Output ("error: " + $_.Exception.Message)
        return $null
    }
}

$c = Probe 'TUNA pytorch-wheels root' 'https://mirrors.tuna.tsinghua.edu.cn/pytorch-wheels/'
if ($c) {
    [regex]::Matches($c, 'href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value } |
        Where-Object { $_ -match 'cu12|cpu' } | Select-Object -First 30
}

$c2 = Probe 'Aliyun pytorch-wheels root' 'https://mirrors.aliyun.com/pytorch-wheels/'
if ($c2) {
    [regex]::Matches($c2, 'href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value } |
        Where-Object { $_ -match 'cu12|cpu|torch_stable' } | Select-Object -First 30
}
