# Multi-stage build for C++ and Python hybrid system
FROM ubuntu:22.04 as cpp-builder

# Install C++ build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    libgmp-dev \
    libgmpxx4ldbl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy C++ source files
COPY *.cpp ./
COPY "finder_new_mersenne prim/"*.cpp ./

# Compile C++ executables
RUN g++ -std=c++17 -O2 -pthread -DUSE_GMP \
    complete_cpp_mersenne_system.cpp \
    -lgmp -lgmpxx \
    -o mersenne_system

RUN g++ -std=c++17 -O2 -pthread \
    optimal_mersenne_engine.cpp \
    -o optimal_mersenne_engine

RUN g++ -std=c++17 -O2 -pthread \
    independent_mersenne_engine.cpp \
    -o independent_mersenne_engine

# Python runtime stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgmp10 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY app.py .
COPY cpp_bridge.py .
COPY templates/ templates/
COPY archived_png_files/ archived_png_files/
COPY *.pdf ./
COPY proofs/ proofs/

# Copy compiled C++ executables from builder stage
COPY --from=cpp-builder /app/mersenne_system .
COPY --from=cpp-builder /app/optimal_mersenne_engine .
COPY --from=cpp-builder /app/independent_mersenne_engine .

# Make executables runnable
RUN chmod +x mersenne_system optimal_mersenne_engine independent_mersenne_engine

# Expose port
EXPOSE 10000

# Start the Flask application
CMD ["python", "app.py"]