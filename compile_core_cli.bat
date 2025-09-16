@echo off
where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo g++ not found. Install MinGW-w64 and add to PATH.
    exit /b 1
)

echo Compiling candidate_generator.cpp ...
g++ -std=c++17 -O3 -march=native -mtune=native -fno-exceptions -fno-rtti -DNDEBUG candidate_generator.cpp -o candidate_generator.exe
if %errorlevel% neq 0 (
    echo Compilation failed.
    exit /b 1
)

echo OK: candidate_generator.exe built

