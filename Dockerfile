# Render Auto-Deploy Dockerfile for C++ Mersenne System
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    libgmp-dev \
    libgmpxx4ldbl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source files
COPY complete_cpp_mersenne_system.cpp .
COPY optimal_mersenne_engine.cpp .
COPY independent_mersenne_engine.cpp .

# Compile the system
RUN g++ -std=c++17 -O2 -pthread -DUSE_GMP \
    complete_cpp_mersenne_system.cpp \
    -lgmp -lgmpxx \
    -o mersenne_system

# Expose port
EXPOSE 8080

# Run the system
CMD ["./mersenne_system"]