# Windows PowerShell setup script for Video Conversation Agent

Write-Host "🎬 Video Conversation Agent - Setup Script" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Check Python version
Write-Host "✓ Checking Python version..." -ForegroundColor Cyan
python --version

# Create virtual environment
Write-Host "✓ Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

# Activate virtual environment
Write-Host "✓ Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "✓ Installing dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt

# Setup environment
Write-Host "✓ Setting up environment..." -ForegroundColor Cyan
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "⚠️  .env file created. Please add your GOOGLE_API_KEY" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Create necessary directories
Write-Host "✓ Creating data directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path logs | Out-Null
New-Item -ItemType Directory -Force -Path data\memory | Out-Null

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your GOOGLE_API_KEY (get from https://ai.google.dev/)"
Write-Host "2. Run: python src/main.py"
Write-Host ""
