### Build and install packages
FROM python:3.9 as build-python

RUN apt-get -y update \
  && apt-get install -y gettext \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/production.txt /app/
COPY requirements/base.txt /app/
WORKDIR /app
RUN pip install -r production.txt

### Final image
FROM python:3.9-slim

RUN groupadd -r loqal && useradd -r -g loqal loqal

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /app/media /app/static \
  && chown -R loqal:loqal /app/

COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY . /app
WORKDIR /app

# RUN SECRET_KEY=dummy python3 manage.py collectstatic --no-input
COPY ./deploy /scripts

RUN chmod +x /scripts/*

EXPOSE 8000
ENV PYTHONUNBUFFERED 1


CMD ["/scripts/entrypoint.sh"]
