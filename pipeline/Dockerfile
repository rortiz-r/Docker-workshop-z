FROM python:3.12

#Copy uv to container

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin/:$PATH"


COPY "pyproject.toml" "uv.lock" ".python-version" ./

COPY pipeline.py .

RUN uv sync --locked

ENTRYPOINT ["python", "pipeline.py"]

