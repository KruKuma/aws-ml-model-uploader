# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# update/upgrade and install tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# generate the machine learning model fit file
# RUN python ./application.py

# launch application
CMD ["python", "application.py"]
