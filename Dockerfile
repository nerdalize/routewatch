FROM python:3.5
MAINTAINER Tim Armstrong
COPY . /RouteWatch
WORKDIR /RouteWatch
EXPOSE 80
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["runserver.py"]
