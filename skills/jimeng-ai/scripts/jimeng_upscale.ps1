# 即梦AI 智能超清 PowerShell 封装脚本
# 用法: .\jimeng_upscale.ps1 -ImagePath "test.jpg" [-Scale 2] [-OutputPath "path"]

param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath,
    
    [int]$Scale = 2,
    
    [string]$OutputPath = ""
)

# 设置输出编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=" * 50
Write-Host "即梦AI - 智能超清" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "输入图片: $ImagePath"
Write-Host "放大倍数: ${Scale}x"
Write-Host ""

# 调用Python脚本
$pythonCmd = "python `"$scriptDir\jimeng_api.py`" upscale --input `"$ImagePath`" --scale $Scale"

if ($OutputPath -ne "") {
    $pythonCmd += " --output `"$OutputPath`""
}

Invoke-Expression $pythonCmd

Write-Host ""
Write-Host "完成!" -ForegroundColor Green
