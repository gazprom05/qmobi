FROM python:latest
COPY qmobi.py /
COPY requirements.txt ./
RUN pip install requests
CMD [ "python", "./qmobi.py" ]