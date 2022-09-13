FROM python:3.10
RUN apt-get update -y
# Get's shared library for zbar
RUN apt-get install -y libzbar0
# Initially encountered an issue that indicated I had to set these ENVs
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install uvicorn
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]