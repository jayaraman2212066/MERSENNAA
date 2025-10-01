@echo off
echo Starting MERSENNE Project with Live C++ Integration...
echo.

REM Start C++ bridge in background
echo Starting C++ Bridge Server...
start /B python cpp_bridge.py

REM Wait for server to start
timeout /t 3 /nobreak >nul

REM Open webpage
echo Opening webpage...
start templates\index.html

echo.
echo Project is now running!
echo - C++ Bridge: http://127.0.0.1:5001
echo - Webpage: templates\index.html
echo.
echo Press any key to stop the C++ bridge...
pause >nul

REM Kill the Python process
taskkill /f /im python.exe >nul 2>&1
echo C++ Bridge stopped.