FROM python:3.9

WORKDIR /

ADD entry.sh /
ADD SolarStats.py /
ADD SolarStatsData.py /
ADD requirements.txt /

RUN pip3 install -r requirements.txt

CMD ["./entry.sh"]


