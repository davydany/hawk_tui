# Use Python 3.12.4 as the base image
FROM python:3.12.4-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Project initialization:
# RUN poetry config virtualenvs.create false
    # && poetry install --no-interaction --no-ansi

# Copy project
COPY . /app

# Install the project
# RUN poetry install

# Make port 80 available to the world outside this container
# EXPOSE 80

# Run the application
# CMD ["poetry", "run", "hawk-tui", "launch", "--tui"]
# CMD ["bash"]

RUN pip install -e /app