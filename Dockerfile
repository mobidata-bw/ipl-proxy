# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cache-mount /root/.cache/pip to speed up subsequent builds.
# Bind-mount requirements.txt to avoid having to copy it.
RUN --mount=type=cache,target=/root/.cache/pip \
	--mount=type=bind,source=requirements.txt,target=requirements.txt \
	pip install -r requirements.txt

COPY . .

CMD ["mitmdump", "-s", "addons.py"]
EXPOSE 8080
