# Stage 1: Build
FROM python:3.11-alpine AS build

WORKDIR /app
COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt \
    && apk del gcc musl-dev python3-dev

# Stage 2: Final
FROM python:3.11-alpine

WORKDIR /app
COPY --from=build /install /usr/local
COPY anekdot.py .

CMD ["python", "anekdot.py"]