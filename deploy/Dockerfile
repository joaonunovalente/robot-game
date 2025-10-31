# ===== Build stage =====
FROM python:3.12-slim AS build

# Install pygbag (and any other deps you need)
RUN pip install --no-cache-dir pygbag

# Set working directory
WORKDIR /app

# Copy your game source files into the image
COPY . .

# Build the game for web
# This creates the /app/build/web directory
RUN pygbag --build main.py

# ===== Serve stage =====
FROM nginx:alpine

# Copy built web files from the previous stage
COPY --from=build /app/build/web /usr/share/nginx/html

# Expose the port Nginx serves on
EXPOSE 80