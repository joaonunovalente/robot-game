# ===== Build stage =====
FROM python:3.12-slim AS build-stage

# Set working directory
WORKDIR /app

# Copy game source files into the image
COPY . .

# Install pygbag & Build the game for web
RUN pip install --no-cache-dir pygbag && \
    pygbag --build main.py

# ===== Serve stage =====
FROM nginx:alpine

# Copy built web files from the previous stage
COPY --from=build-stage /app/build/web /usr/share/nginx/html

# Expose the port Nginx serves on
EXPOSE 80