# Use the official Python base image
FROM python:3.10-alpine3.16 AS python-base

# Copy requirements.txt first to avoid dependency issues
COPY requirements.txt /code/requirements.txt

# Install dependencies for Gitleaks and Python
RUN apk add --no-cache bash curl git && pip install --no-cache-dir -r /code/requirements.txt

# Use Gitleaks base image
FROM zricethezav/gitleaks:latest AS gitleaks-base

# Combine both images into the final stage
FROM python-base AS final-image

# Copy the necessary files
COPY --from=gitleaks-base /usr/bin/gitleaks /usr/bin/gitleaks
COPY transform.py /code/transform.py
COPY gitleaks_proccessor.py /code/gitleaks_proccessor.py
COPY utils/ /code/utils/

# Set working directory
WORKDIR /code

# Set the Python script as the entry point
ENTRYPOINT ["python", "/code/gitleaks_proccessor.py"]
