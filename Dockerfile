# start by pulling the python image
FROM python:3.8-alpine

ENV VIRTUAL_ENV=/molreport/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=:/url-shortener-plus/app

# copy the requirements file into the image
COPY ./requirements.txt /url-shortener-plus/requirements.txt

# switch working directory
WORKDIR /url-shortener-plus

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /url-shortener-plus

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["application.py"]