from ubuntu

# Set an environment variable to prevent debian warning.
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN apt update && apt upgrade -y
RUN apt install python3  nodejs ffmpeg npm python3-pip -y

# setup chromium
## Copy apt configs
COPY ./build_files/debian.list /etc/apt/sources.list.d/debian.list
COPY ./build_files/chromium.pref /etc/apt/preferences.d/chromium.pref

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys AA8E81B4331F7F50
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A

RUN apt update && apt install -y chromium
RUN ln -s /usr/bin/chromium /usr/bin/chromium-browser
RUN npm install --global yarn

RUN apt install -y postgresql-client  libpq-dev
RUN useradd -m app

COPY ./requeriments.txt /
RUN pip install -r /requeriments.txt

WORKDIR /home/app


# copy bbb-video project
COPY ./bbb-video-download/src/package.json ./
RUN yarn install 
COPY ./bbb-video-download/src ./bbb-video-download

COPY ./entrypoint.sh ./entrypoint.sh
run mkdir /home/app/media
run chown app:app -R /home/app
run chown app:app -R /home/app/media
USER app

#COPY ./lassar-api /app/lassar-api

CMD ["./entrypoint.sh"]
