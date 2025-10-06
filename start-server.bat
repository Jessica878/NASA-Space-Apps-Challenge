@echo off
echo Starting EmbiggenEye Web Server...
echo.
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "simple-server.ps1"
pause