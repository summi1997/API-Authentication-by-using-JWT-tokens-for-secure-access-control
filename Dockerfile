FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Use absolute path and explicit host binding
CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]