# 即梦AI 文生图 PowerShell 封装脚本
# 用法: .\jimeng_text2image.ps1 -Prompt "描述" [-AspectRatio "16:9"] [-OutputPath "path"]

param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt,
    
    [string]$AspectRatio = "1:1",
    
    [string]$OutputPath = "",
    
    [int]$ImageNum = 1,
    
    [string]$ModelVersion = "general-v3.1"
)

# 设置输出编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=" * 50
Write-Host "即梦AI - 文生图" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "提示词: $Prompt"
Write-Host "宽高比: $AspectRatio"
Write-Host "生成数量: $ImageNum"
Write-Host ""

# 调用Python脚本
$pythonCmd = "python `"$scriptDir\jimeng_api.py`" text2image --prompt `"$Prompt`" --ratio `"$AspectRatio`" --num $ImageNum --model `"$ModelVersion`""

if ($OutputPath -ne "") {
    $pythonCmd += " --output `"$OutputPath`""
}

Invoke-Expression $pythonCmd

Write-Host ""
Write-Host "完成!" -ForegroundColor Green
