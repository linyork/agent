# Run code quality checks using ruff

Write-Host "Running code quality checks..." -ForegroundColor Cyan

# Check if uv is installed
if (!(Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Error "uv command not found. Please install uv first."
    exit 1
}

# Run ruff check
Write-Host "1. Linting (Ruff)..." -ForegroundColor Yellow
uv run ruff check src tests

if ($LASTEXITCODE -ne 0) {
    Write-Host "Lint check failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# Run ruff format check
Write-Host "2. Formatting Check..." -ForegroundColor Yellow
uv run ruff format --check src tests

if ($LASTEXITCODE -eq 0) {
    Write-Host "All checks passed!" -ForegroundColor Green
}
else {
    Write-Host "Format check failed. Run 'uv run ruff format' to auto-fix." -ForegroundColor Red
    exit $LASTEXITCODE
}
