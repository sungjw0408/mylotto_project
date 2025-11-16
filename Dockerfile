# 베이스 이미지 선택
FROM python:3.12-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# 작업 디렉토리 설정
WORKDIR /app

# 라이브러리
COPY requirements.txt .
RUN pip install -r requirements.txt

# 프로젝트 코드 
COPY . .

# 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]