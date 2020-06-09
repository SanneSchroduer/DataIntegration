FROM python:3.6
EXPOSE 5000
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt
CMD cd modules && python app.py
