FROM python:3.10-slim
WORKDIR /lc-geo
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["python", "src/server.py"]