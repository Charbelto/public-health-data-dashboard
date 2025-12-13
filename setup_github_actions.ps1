# Setup script for GitHub Actions - Windows PowerShell

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "GitHub Actions Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "[OK] Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if already a git repository
if (Test-Path ".git") {
    Write-Host "[OK] Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
}

# Check for GitHub remote
$remotes = git remote
if ($remotes -contains "origin") {
    Write-Host "[OK] Remote 'origin' already configured" -ForegroundColor Green
    git remote -v
} else {
    Write-Host ""
    Write-Host "No remote repository configured." -ForegroundColor Yellow
    Write-Host "Please enter your GitHub repository URL:"
    Write-Host "Example: https://github.com/username/public-health-data-dashboard.git" -ForegroundColor Cyan
    $repoUrl = Read-Host "Repository URL"
    
    if ($repoUrl) {
        git remote add origin $repoUrl
        Write-Host "[OK] Remote 'origin' added: $repoUrl" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] No repository URL provided. You can add it later with:" -ForegroundColor Yellow
        Write-Host "   git remote add origin <url>" -ForegroundColor Gray
    }
}

# Check for staged changes
Write-Host ""
Write-Host "Checking for changes..." -ForegroundColor Yellow
$status = git status --porcelain

if ($status) {
    Write-Host "[INFO] Uncommitted changes detected" -ForegroundColor Yellow
    Write-Host ""
    $commitChoice = Read-Host "Would you like to commit all changes? (y/n)"
    
    if ($commitChoice -eq "y" -or $commitChoice -eq "Y") {
        git add .
        git commit -m "Add GitHub Actions workflows for automated testing"
        Write-Host "[OK] Changes committed" -ForegroundColor Green
    }
} else {
    Write-Host "[OK] No uncommitted changes" -ForegroundColor Green
}

# Push to GitHub
Write-Host ""
$pushChoice = Read-Host "Would you like to push to GitHub now? (y/n)"

if ($pushChoice -eq "y" -or $pushChoice -eq "Y") {
    # Get current branch
    $currentBranch = git branch --show-current
    
    if (-not $currentBranch) {
        # No branch yet, create main branch
        git branch -M main
        $currentBranch = "main"
    }
    
    Write-Host "Pushing to branch: $currentBranch" -ForegroundColor Cyan
    git push -u origin $currentBranch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[SUCCESS] Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Cyan
        Write-Host "Next Steps:" -ForegroundColor Cyan
        Write-Host "==========================================" -ForegroundColor Cyan
        Write-Host "1. Go to your GitHub repository"
        Write-Host "2. Click on the 'Actions' tab"
        Write-Host "3. You should see workflows running automatically"
        Write-Host "4. Update badge URLs in README.md with your username"
        Write-Host ""
        Write-Host "Workflows configured:" -ForegroundColor Yellow
        Write-Host "  - Run Tests (Multi-platform, Multi-version)"
        Write-Host "  - Quick Test (Fast feedback)"
        Write-Host "  - Linting (Code quality)"
        Write-Host ""
        Write-Host "For more details, see CI_SETUP_COMPLETE.md"
        Write-Host "==========================================" -ForegroundColor Cyan
    } else {
        Write-Host "[ERROR] Failed to push. Please check your credentials and remote URL." -ForegroundColor Red
    }
} else {
    Write-Host "[INFO] Skipped push. You can push later with:" -ForegroundColor Yellow
    Write-Host "   git push -u origin main" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[COMPLETE] Setup complete!" -ForegroundColor Green
