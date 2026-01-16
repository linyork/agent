# Run all tests using pytest

Write-Host "Running tests..." -ForegroundColor Cyan

# Check if uv is installed
if (!(Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Error "uv command not found. Please install uv first."
    exit 1
}

# Run pytest with verbose output and short traceback
uv run pytest -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
}
else {
    Write-Host "Tests failed. Please check the error messages." -ForegroundColor Red
    exit $LASTEXITCODE
}
