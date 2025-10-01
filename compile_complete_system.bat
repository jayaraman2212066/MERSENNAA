@echo off
echo 🚀 COMPILING COMPLETE C++ MERSENNE SYSTEM 🚀
echo Pure C++ - No Python dependencies - Prime95 equivalent

REM Check for GMP
if exist "C:\msys64\mingw64\include\gmp.h" (
    set GMP_PATH=C:\msys64\mingw64
    set USE_GMP=1
) else if exist "C:\MinGW\include\gmp.h" (
    set GMP_PATH=C:\MinGW
    set USE_GMP=1
) else (
    set USE_GMP=0
)

echo 📦 Compiling complete system with maximum optimization...

if %USE_GMP%==1 (
    echo ✅ Using GMP for Prime95-equivalent performance
    g++ -std=c++17 -O3 -march=native -mtune=native -flto ^
        -funroll-loops -ffast-math -DNDEBUG -DUSE_GMP ^
        -pthread -fopenmp ^
        -I"%GMP_PATH%\include" -L"%GMP_PATH%\lib" ^
        complete_cpp_mersenne_system.cpp ^
        -lgmp -lgmpxx -lws2_32 ^
        -o mersenne_system.exe
) else (
    echo ⚠️ GMP not found - using optimized fallback
    g++ -std=c++17 -O3 -march=native -mtune=native -flto ^
        -funroll-loops -ffast-math -DNDEBUG ^
        -pthread -fopenmp ^
        complete_cpp_mersenne_system.cpp ^
        -lws2_32 ^
        -o mersenne_system.exe
)

if %errorlevel% equ 0 (
    echo ✅ Complete C++ system compiled successfully!
    echo 🎯 Executable: mersenne_system.exe
    echo 🌐 Web interface: http://localhost:8080
    echo 🚀 Starting complete system...
    mersenne_system.exe
) else (
    echo ❌ Compilation failed - trying basic version
    g++ -std=c++17 -O2 -pthread ^
        complete_cpp_mersenne_system.cpp ^
        -lws2_32 ^
        -o mersenne_system_basic.exe
    
    if %errorlevel% equ 0 (
        echo ✅ Basic version compiled
        mersenne_system_basic.exe
    )
)

pause