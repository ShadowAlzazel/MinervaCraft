# Stage 1: Build the bot app
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies for Python and Node.js
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Copy and install Python dependencies
COPY requirements.txt . 
RUN pip install -r requirements.txt

# Run the builder for node modules
COPY builder.py .
RUN python -m javascript --install mineflayer
RUN python -m javascript --install minecraft-data
RUN python -m javascript --install prismarine-item
RUN python -m javascript --install mineflayer-pathfinder
RUN python -m javascript --install mineflayer-pvp
RUN python -m javascript --install mineflayer-collectblock
RUN python -m javascript --install mineflayer-auto-eat
RUN python -m javascript --install mineflayer-armor-manager
RUN python -m javascript --install mineflayer-tool
RUN python builder.py

# Copy the application source code
COPY ./src ./src
COPY ./profiles ./profiles
COPY main.py . 
COPY keys.json . 
COPY settings.py .

# Stage 2: Create the runtime image
FROM python:3.12-slim AS runner

WORKDIR /app
COPY --from=builder /app /app

EXPOSE 8000

CMD ["python", "main.py"]