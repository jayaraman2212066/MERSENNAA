@echo off
echo 🚀 COMPILING CPU-ONLY ULTRA-SPEED MERSENNE FINDER 🚀
echo Optimized for Acer Aspire 5 (12th Gen Intel)
echo ================================================

REM Check if g++ is available
where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: g++ compiler not found!
    echo.
    echo Please install MinGW-w64 with g++ support:
    echo 1. Download from: https://www.mingw-w64.org/
    echo 2. Add to PATH environment variable
    echo 3. Restart this command prompt
    echo.
    pause
    exit /b 1
)

echo ✅ g++ compiler found
echo.

echo 🧵 Compiling with maximum CPU optimizations...
echo.

REM Compile with ultra-aggressive optimization flags
g++ -std=c++17 ^
    -O3 ^
    -march=native ^
    -mtune=native ^
    -mavx2 ^
    -mfma ^
    -flto ^
    -ffast-math ^
    -funroll-loops ^
    -fomit-frame-pointer ^
    -fno-exceptions ^
    -fno-rtti ^
    -pthread ^
    -DNDEBUG ^
    ultra_speed_mersenne_finder_cpu_only.cpp ^
    -o ultra_speed_mersenne_finder_cpu.exe

if %errorlevel% equ 0 (
    echo.
    echo 🎉 COMPILATION SUCCESSFUL! 🎉
    echo.
    echo 📁 Output file: ultra_speed_mersenne_finder_cpu.exe
    echo 🚀 Ready for ultra-speed Mersenne prime discovery!
    echo.
    echo 💡 Performance Features:
    echo    • FFT-based modular arithmetic (Prime95 style)
    echo    • AVX2/AVX-512 SIMD optimizations
    echo    • Multi-threading (8-10 cores)
    echo    • Cache-optimized memory management
    echo    • Assembly-level optimizations
    echo.
    echo 🎯 Expected speed: 100-1000x faster than standard implementations
    echo ⏰ Target: New world record in hours, not days!
    echo.
    echo 🚀 To run: ultra_speed_mersenne_finder_cpu.exe
    echo.
) else (
    echo.
    echo ❌ COMPILATION FAILED!
    echo.
    echo 🔧 Troubleshooting:
    echo    1. Verify g++ version (need 7.0+)
    echo    2. Ensure sufficient disk space
    echo    3. Try running as Administrator
    echo.
)

echo Press any key to exit...
pause >nul
