@echo off
echo 🚀 COMPILING INDEPENDENT MERSENNE ENGINE 🚀

REM Check if compiler exists
where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Error: g++ compiler not found
    echo Please install MinGW-w64 or similar
    pause
    exit /b 1
)

echo 📦 Compiling independent engine with maximum optimizations...

REM Compile with all optimizations
g++ -std=c++17 -O3 -march=native -mtune=native -flto ^
    -funroll-loops -ffast-math -DNDEBUG ^
    -fopenmp -pthread ^
    -mavx2 -mfma ^
    independent_mersenne_engine.cpp ^
    -o independent_mersenne_engine.exe

if %errorlevel% equ 0 (
    echo ✅ Compilation successful!
    echo 🎯 Executable: independent_mersenne_engine.exe
    echo.
    echo 🚀 Running independent engine...
    independent_mersenne_engine.exe
) else (
    echo ❌ Compilation failed!
    echo.
    echo 🔧 Trying fallback compilation...
    g++ -std=c++17 -O2 -pthread ^
        independent_mersenne_engine.cpp ^
        -o independent_mersenne_engine_basic.exe
    
    if %errorlevel% equ 0 (
        echo ✅ Fallback compilation successful!
        echo 🎯 Executable: independent_mersenne_engine_basic.exe
        independent_mersenne_engine_basic.exe
    ) else (
        echo ❌ All compilation attempts failed!
    )
)

pause