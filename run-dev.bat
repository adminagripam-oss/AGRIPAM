@echo off
title AGRI-PAM Local Dev Server
echo ============================================================
echo   AGRI-PAM Local Dev Server
echo ============================================================
echo.
echo Installing dependencies (if any)...
call npm install
echo.
echo Starting development server...
node dev-server.js
if errorlevel 1 (
    echo.
    echo Server crashed or Node.js is not installed.
    echo Please make sure Node.js is installed (https://nodejs.org/).
)
pause
