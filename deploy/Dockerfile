# Use Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the fully built game folder
COPY build/web ./build/web

# Expose port
EXPOSE 8000

# Serve the game
CMD ["python3", "-m", "http.server", "8000", "--bind", "0.0.0.0", "--directory", "build/web"]
