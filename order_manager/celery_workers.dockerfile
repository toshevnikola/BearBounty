FROM python:3.8

WORKDIR /order_manager/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . ./
RUN chmod +x /order_manager/worker-start.sh

CMD ["bash", "/order_manager/worker-start.sh"]
