FROM debian:bullseye-slim

COPY . .

RUN apt update && apt install -y gcc-x86-64-linux-gnu g++-x86-64-linux-gnu make && apt install -y python3.9-dev python3-venv python3-setuptools
RUN apt install -y wget apt-transport-https gnupg && wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && apt update && apt install -y temurin-17-jdk

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

RUN pip install fastapi[all]

RUN wget https://archive.apache.org/dist/lucene/java/9.12.0/lucene-9.12.0-src.tgz && tar -xzvf lucene-9.12.0-src.tgz && mv lucene-9.12.0 lucene-9.12.0-src
RUN wget https://archive.apache.org/dist/lucene/java/9.12.0/lucene-9.12.0.tgz && tar -xzvf lucene-9.12.0.tgz
RUN wget https://dlcdn.apache.org/lucene/pylucene/pylucene-9.12.0-src.tar.gz && tar -xzvf pylucene-9.12.0-src.tar.gz

RUN mv -f Makefile ./pylucene-9.12.0/Makefile

WORKDIR /pylucene-9.12.0/jcc
RUN python setup.py build && python setup.py install

WORKDIR /pylucene-9.12.0
RUN make && make install

WORKDIR /app
RUN python IndexDocsFiles.py && python IndexSourceFiles.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
