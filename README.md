# dockerized-pylucene
Dockerized PyLucene environment for documents and source code search experimentation.

문서 및 소스 코드 검색 실험을 위한 Docker 기반 PyLucene 실행 환경 구축

# 포함된 기능
📦 PyLucene, Apache Lucene, FastAPI 패키지 구조가 매우 정돈됨
🐳 Dockerfile 에 PyLucene 빌드 과정과 의존성 정보 모두 포함
📖 Documents 와 Java Source Code 를 검색할 수 있는 웹서버 실행
💡 Java Lucene 대신 Python에서 Lucene 사용
✨ PyLucene 빌드 자동화

# 폴더 구조
```
dockerized-pylucene/
│
├── pylucene-docker-image/
│   └── app/
│       ├── templates
│       ├── main.py
│       ├── IndexDocsFiles.py
│       └── IndexSourceFiles.py
│   ├── Makefile
│   ├── Dockerfile
├── README.md
```

# 기술 스택
- Python
- PyLucene
- Docker
- JCC
- Apache Lucene
- Java
- GCC/G++
- Debian

# 실행 방법
## 도커 이미지 빌드
```
docker build -t pylucene-docker-image ./dockerized-pylucene/pylucene-docker-image/
```

## 도커 컨테이너 실행
```
docker run --name debian-pylucene-fastapi -p 5000:8000 pylucene-docker-image
```

## 웹서버 접속
```
localhost:5000/search?query=lucene
```
