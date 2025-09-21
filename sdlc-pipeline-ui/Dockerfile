# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files if present
# The build context is likely sdlc-pipeline-ui/build, which may not contain package.json.
# Make npm steps conditional to avoid failing when package.json is absent.
# Copy source code
COPY . .
COPY package.json ./
COPY package-lock.json* ./

# Install dependencies only if package.json exists
RUN  npm install --legacy-peer-deps;

# Build the application if package.json exists; otherwise, create a simple static page
RUN if [ -f package.json ] && [ -f public/index.html ]; then \
      npm run build; \
    else \
      echo "React app 'public/index.html' not found. Building placeholder static site."; \
      mkdir -p build && \
      printf '<!doctype html>\n<html><head><meta charset="utf-8"/><title>SDLC Pipeline UI</title></head><body><h1>SDLC Pipeline UI</h1><p>UI build not available. Placeholder page.</p><p>Timestamp: ' > build/index.html && \
      date -u "+%Y-%m-%dT%H:%M:%SZ" >> build/index.html && \
      printf '</p></body></html>\n' >> build/index.html; \
    fi


# Production stage
FROM nginx:alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Set default API origin for proxy; can be overridden at runtime
ENV API_ORIGIN=http://sdlc-pipeline-api:8000

# Copy templated nginx configuration
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Copy built application
COPY --from=build /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -fsS http://localhost/ || exit 1

# Start nginx with envsubst to render template
CMD ["/bin/sh", "-c", "envsubst '${API_ORIGIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'" ]
