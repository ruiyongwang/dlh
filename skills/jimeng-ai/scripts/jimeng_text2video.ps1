# 即梦AI 文生视频 PowerShell 封装脚本
# 用法: .\jimeng_text2video.ps1 -Prompt "描述" [-Duration 5] [-OutputPath "path"]

param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt,
    
    [int]$Duration = 5,
    
    [string]$OutputPath = ""
)

# 设置输出编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=" * 50
Write-Host "即梦AI - 文生视频" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "提示词: $Prompt"
Write-Host "时长: ${Duration}秒"
Write-Host ""

# 调用Python脚本
$pythonCmd = "python `"$scriptDir\jimeng_api.py`" text2video --prompt `"$Prompt`" --duration $Duration"

if ($OutputPath -ne "") {
    $pythonCmd += " --output `"$OutputPath`""
}

Invoke-Expression $pythonCmd

Write-Host ""
Write-Host "完成!" -ForegroundColor Green
