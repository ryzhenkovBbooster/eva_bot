FROM python:3.11
WORKDIR /app
RUN chmod 755 .

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY /modif/__init__.py /usr/local/lib/python3.11/site-packages/aioschedule/__init__.py
COPY . .