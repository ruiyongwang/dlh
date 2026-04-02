# Duliangheng Think Tank - GitHub Upload Script
# Upload dlh-skills to GitHub

param(
    [string]$RepoOwner = "ruiyongwang",
    [string]$RepoName = "dlh",
    [string]$Branch = "main",
    [switch]$SkipGitHub = $false
)

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Duliangheng Think Tank - GitHub Upload" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Git
Write-Host "[1/5] Checking Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Please install from: https://git-scm.com" -ForegroundColor Red
    exit 1
}
Write-Host "Git OK" -ForegroundColor Green

# 2. Check gh CLI
Write-Host "[2/5] Checking GitHub CLI..." -ForegroundColor Yellow
$ghAvailable = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghAvailable) {
    Write-Host "GitHub CLI not found, will use Git method" -ForegroundColor Yellow
    $useGh = $false
} else {
    Write-Host "GitHub CLI OK" -ForegroundColor Green
    $useGh = $true
}

# 3. Prepare local repo
Write-Host "[3/5] Preparing local repo..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsDir = Join-Path $scriptDir "skills"
$readmePath = Join-Path $scriptDir "README.md"
$readmeEnPath = Join-Path $scriptDir "README_en.md"

if (-not (Test-Path $skillsDir)) {
    Write-Host "Error: skills directory not found" -ForegroundColor Red
    exit 1
}

$skillCount = (Get-ChildItem -Path $skillsDir -Directory).Count
Write-Host "Found $skillCount skills" -ForegroundColor Green

# 4. GitHub Operations
if (-not $SkipGitHub) {
    if ($useGh) {
        Write-Host "[4/5] GitHub Operations (using gh CLI)..." -ForegroundColor Yellow

        # Check auth status
        $ghStatus = gh auth status 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Please login to GitHub first: gh auth login" -ForegroundColor Red
            Write-Host "Then re-run this script" -ForegroundColor Red
            exit 1
        }

        # Fork repo
        $repoExists = gh repo view "$RepoOwner/$RepoName" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Forking repo..." -ForegroundColor Yellow
            gh repo fork "ruiyongwang/dlh" --clone
        } else {
            Write-Host "Repo exists" -ForegroundColor Green
        }

        # Clone and update
        $tempDir = Join-Path $env:TEMP "dlh-github-upload"
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force
        }
        gh repo clone "$RepoOwner/$RepoName" $tempDir

        # Copy files
        Copy-Item -Path $skillsDir -Destination (Join-Path $tempDir "skills") -Recurse -Force
        if (Test-Path $readmePath) {
            Copy-Item -Path $readmePath -Destination $tempDir -Force
        }
        if (Test-Path $readmeEnPath) {
            Copy-Item -Path $readmeEnPath -Destination $tempDir -Force
        }

        # Commit
        Set-Location $tempDir
        git add .
        $commitMsg = "feat: publish Duliangheng OpenClaw skills pack ($(Get-Date -Format 'yyyy-MM-dd'))"
        git commit -m $commitMsg

        # Push
        git push origin $Branch
        Set-Location $scriptDir

        Write-Host "Upload successful!" -ForegroundColor Green
        Write-Host "Repo: https://github.com/$RepoOwner/$RepoName" -ForegroundColor Cyan

    } else {
        Write-Host "[4/5] GitHub Operations (using Git)..." -ForegroundColor Yellow
        Write-Host "Please complete the following steps manually:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  1. Fork: https://github.com/ruiyongwang/dlh" -ForegroundColor Cyan
        Write-Host "  2. Clone your fork:"
        Write-Host "     git clone https://github.com/YOUR_USERNAME/dlh.git" -ForegroundColor Cyan
        Write-Host "  3. Copy skills folder to repo" -ForegroundColor Cyan
        Write-Host "  4. Commit and push:"
        Write-Host "     git add ." -ForegroundColor Cyan
        Write-Host "     git commit -m 'feat: publish skills'" -ForegroundColor Cyan
        Write-Host "     git push origin main" -ForegroundColor Cyan
        Write-Host ""
    }
} else {
    Write-Host "[4/5] Skip GitHub operations" -ForegroundColor Yellow
}

# 5. Done
Write-Host "[5/5] Done!" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Package ready" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Package path: $scriptDir" -ForegroundColor White
Write-Host "Skills count: $skillCount" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Fork https://github.com/ruiyongwang/dlh" -ForegroundColor White
Write-Host "  2. Upload skills folder content" -ForegroundColor White
Write-Host "  3. Create Pull Request" -ForegroundColor White
Write-Host ""
