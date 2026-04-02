# 即梦AI 图生图 PowerShell 封装脚本
# 用法: .\jimeng_image2image.ps1 -ImagePath "test.jpg" -Prompt "描述" [-OutputPath "path"]

param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath,
    
    [Parameter(Mandatory=$true)]
    [string]$Prompt,
    
    [string]$OutputPath = ""
)

# 设置输出编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=" * 50
Write-Host "即梦AI - 图生图" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "输入图片: $ImagePath"
Write-Host "修改描述: $Prompt"
Write-Host ""

# 调用Python脚本
$pythonCmd = "python `"$scriptDir\jimeng_api.py`" image2image --input `"$ImagePath`" --prompt `"$Prompt`""

if ($OutputPath -ne "") {
    $pythonCmd += " --output `"$OutputPath`""
}

Invoke-Expression $pythonCmd

Write-Host ""
Write-Host "完成!" -ForegroundColor Green
