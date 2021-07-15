FROM python:tagname
ENV PYTHONUNBUFFERED=1
WORKDIR /code/ecommerce
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
