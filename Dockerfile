FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask gunicorn
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]