# Stage 1: Build MkDocs static site
FROM python:3.11-slim AS builder

WORKDIR /docs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mkdocs.yml .
COPY docs/ docs/

RUN mkdocs build --strict

# Stage 2: Serve with rootless Nginx on an unprivileged port
FROM nginxinc/nginx-unprivileged:alpine

COPY --from=builder /docs/site /usr/share/nginx/html

EXPOSE 8080
