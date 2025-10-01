# Simple Python-only deployment
FROM python:3.11-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Copy directories that exist
COPY templates/ templates/
COPY archived_png_files/ archived_png_files/

# Copy PDFs if they exist
COPY *.pdf ./ || true

# Expose port
EXPOSE 10000

# Start the Flask application
CMD ["python", "app.py"]