FROM ubuntu:22.04
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip \
    libegl1 \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/lists/*
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
RUN [ "chmod", "+x", "__main__.py" ]
RUN [ "mkdir", "/io" ]
WORKDIR /io
ENTRYPOINT ["python3", "/usr/src/app"]