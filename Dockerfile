FROM python:3.6
ADD . /api
WORKDIR /api
RUN pip install -r requirements.txt
CMD python -m flask run --host='0.0.0.0'