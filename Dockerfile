##### Base Layer #####

# Apply python-base image
FROM python:3.10.7-slim-buster as python-base

# Install extra libraries
RUN apt-get update -yqq \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    libssl-dev \
    libboost-all-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.2.2 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

##### Builder Base Layer #####

# "builder" stage uses "python-base" stage to install app depedencies
FROM python-base as app-builder
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry (uses $POETRY_HOME & $POETRY_VERSION environment variables)
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# Copy Python requirements and install only runtime dependencies
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

##### Application Layer (--target application) #####

# "application" stage uses "python-base" stage and copies in app dependencies from "app-builder"
FROM python-base as application

EXPOSE 8000

# Copy "app-builder" layer python environment into application layer
COPY --from=app-builder $VENV_PATH $VENV_PATH

# Set active directory
WORKDIR /app

# Add non-root user
RUN adduser --disabled-password --gecos '' appuser

# Change owner to non-root user
RUN chown appuser \
    /app \
    /var/run

# Copy configuration components then application code
COPY /conf/gunicorn_conf.py \
     /conf/start.sh \
     /conf/test_runner.sh ./
COPY /app ./app
COPY /main.py ./app

# Assign start shell script permission privilege to non-root user
RUN chmod +x /app/start.sh /app/test_runner.sh

# Set non-root user
USER appuser

# Set default command to start shell command
CMD ["/app/start.sh"]

##### Test-Builder Layer #####

# "test-builder" stage uses "builder" stage and install test dependencies
FROM app-builder as test-builder

# Install the other dev dependencies originally skipped via the poetry "--no-dev" install flag
WORKDIR $PYSETUP_PATH
RUN poetry install

##### Testing Layer (--target testing) #####

# "testing" stage uses "application" stage and adds test dependencies to execute test script
FROM application as testing

# Copy test-builder python env into testing layer
COPY --from=test-builder $VENV_PATH $VENV_PATH

# Set active directory and copy test dependencies
WORKDIR /app
COPY /tests ./tests

# Set default to command run tests
CMD ["/app/test_runner.sh"]
