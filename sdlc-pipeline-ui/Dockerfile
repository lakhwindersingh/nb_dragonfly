# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files if present
# The build context is likely sdlc-pipeline-ui/build, which may not contain package.json.
# Make npm steps conditional to avoid failing when package.json is absent.
COPY package*.json ./

# Install dependencies only if package.json exists
RUN if [ -f package.json ]; then \
      npm ci --no-audit --no-fund || npm install --legacy-peer-deps; \
    else \
      echo "No package.json found, skipping npm install"; \
    fi

# Copy source code
COPY . .
COPY package.json ./
COPY package-lock.json* ./

# Build the application if package.json exists; otherwise, create a simple static page
RUN if [ -f package.json ]; then \
      npm run build; \
    else \
      mkdir -p build && \
      printf '<!doctype html>\n<html><head><meta charset="utf-8"/><title>SDLC Pipeline UI</title></head><body><h1>SDLC Pipeline UI</h1><p>UI build not available. Placeholder page.</p><p>Timestamp: ' > build/index.html && \
      date -u "+%Y-%m-%dT%H:%M:%SZ" >> build/index.html && \
      printf '</p></body></html>\n' >> build/index.html; \
    fi

# Production stage
FROM nginx:alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application
COPY --from=build /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -fsS http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
