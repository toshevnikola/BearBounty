FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app/
COPY ./app/requirements.txt /app/requirements.txt
RUN pip3 install --requirement /app/requirements.txt
ENV PYTHONPATH=/app
COPY ./app /app