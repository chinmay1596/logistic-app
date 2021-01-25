FROM python:3.6
RUN apt-get update
ENV PYTHONUNBUFFERED 1
RUN mkdir /Halo_logistics
WORKDIR /Halo_logistics
RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
COPY package.json /Halo_logistics/
RUN npm install
COPY requirements.txt /Halo_logistics/
RUN pip install -r requirements.txt
COPY . /Halo_logistics/
