FROM       ubuntu:latest
MAINTAINER Aaron Rosen <aaronorosen@gmail.com>
RUN apt-get update
RUN apt-get install -y python-pip wget git
RUN pip install flask
RUN pip install twilio
RUN  mkdir -p /opt
RUN git clone https://github.com/aaronorosen/vmworld_demo /opt/vmworld_demo
CMD python /opt/vmworld_demo/twilio_server.py
EXPOSE 5000
