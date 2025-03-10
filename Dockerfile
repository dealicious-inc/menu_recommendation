# Base image 선택
FROM python:3.12-slim

# 타임존 설정
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages --ignore-installed

COPY . .

# 애플리케이션 실행
ENTRYPOINT ["python", "main.py"]