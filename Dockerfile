FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN [ "chmod", "+x", "__main__.py" ]
RUN [ "mkdir", "/input" ]
WORKDIR /io
ENTRYPOINT [ "python", "/usr/src/app" ]