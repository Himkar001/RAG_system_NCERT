$ErrorActionPreference = "Stop"

Write-Host "Starting RAG System (Development Mode)" -ForegroundColor Green

# Activate virtual environment
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    . $venvPath
    Write-Host "Activated virtual environment." -ForegroundColor Cyan
} else {
    Write-Warning "Virtual environment not found at $venvPath"
}

# Start backend in a new process
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process -FilePath "uvicorn" -ArgumentList "backend.main:app", "--reload", "--port", "8000" -NoNewWindow

# Start frontend in a new process
Write-Host "Starting frontend dev server..." -ForegroundColor Cyan
Set-Location -Path "frontend"
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -NoNewWindow
Set-Location -Path ".."

Write-Host "Servers are starting up..." -ForegroundColor Yellow
Write-Host "Backend URL: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend URL: http://localhost:5173 (default for Vite)" -ForegroundColor Yellow
Write-Host "Press Ctrl+C in the respective terminal windows to stop the servers." -ForegroundColor Yellow
