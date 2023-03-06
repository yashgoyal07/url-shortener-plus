# start by pulling the python image
FROM python:3.8-alpine

# add every content from the local file to the image
ADD . /url-shortener-plus

# switch working directory
WORKDIR /url-shortener-plus

# add pythonpath
ENV PYTHONPATH=:/url-shortener-plus/app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["application.py"]