# syntax=docker/dockerfile:1

FROM python:3.13-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
	netcat-openbsd \
	&& rm -rf /var/lib/apt/lists/*

# Cache-mount /root/.cache/pip to speed up subsequent builds.
# Bind-mount requirements.txt to avoid having to copy it.
RUN --mount=type=cache,target=/root/.cache/pip \
	--mount=type=bind,source=requirements.txt,target=requirements.txt \
	pip install -r requirements.txt

COPY . .

ENV LOG_LEVEL=info

CMD [\
	"/bin/sh", "-u", "-c", \
	# > Log verbosity.
	# > Default: info
	# > Choices: error, warn, info, alert, debug
	# > Flow Detail
	# > Default: 1
	# > Choices: 0, 1, 2, 3, 4
	# > Set to 0, because request logging is done by addons.py
	# https://docs.mitmproxy.org/stable/concepts-options/#available-options
	"mitmdump -s addons.py --set termlog_verbosity=$LOG_LEVEL --set flow_detail=0" \
]

# When sending an HTTP request with `Host: localhost`, mitmproxy will respond with 502.
# So we only check if there's a process listening on that port.
HEALTHCHECK --start-period=5s --timeout=1s --interval=5s --retries=5 CMD ["nc", "-z", "localhost", "8080"]

EXPOSE 8080
