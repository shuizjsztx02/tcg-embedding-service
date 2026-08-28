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

$urls = @(
  'https://mirrors.tuna.tsinghua.edu.cn/pytorch-wheels/cu124/torch-2.13.0%2Bcu124-cp313-cp313-manylinux_2_28_x86_64.whl',
  'https://mirrors.aliyun.com/pytorch-wheels/cu124/torch-2.13.0%2Bcu124-cp313-cp313-manylinux_2_28_x86_64.whl'
)
foreach ($u in $urls) {
    Write-Output ("CHECK " + $u)
    try {
        $h = Invoke-WebRequest -Uri $u -Method Head -UseBasicParsing -TimeoutSec 45
        $len = $h.Headers['Content-Length']
        Write-Output ("  status=" + $h.StatusCode + " bytes=" + $len)
    } catch {
        Write-Output ("  error: " + $_.Exception.Message)
    }
}

$c2 = Probe 'Aliyun pytorch-wheels root' 'https://mirrors.aliyun.com/pytorch-wheels/'
if ($c2) {
    [regex]::Matches($c2, 'href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value } |
        Where-Object { $_ -match 'cu124|torch_stable' } | Select-Object -First 20
}
