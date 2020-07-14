FROM python:3.7

RUN pip install uwsgi==2.0.17.1
WORKDIR stockprice_crawler

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD uwsgi.ini uwsgi.ini
EXPOSE 80

ADD . .

ENV FLASK_APP wsgi.py
CMD flask db upgrade \
 && uwsgi uwsgi.ini
