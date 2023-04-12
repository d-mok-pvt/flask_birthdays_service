FROM alpine:latest

ARG JMETER_VERSION="5.5"
ENV TZ=Asia/Dubai
ENV JMETER_HOME /opt/apache-jmeter-${JMETER_VERSION}
ENV JMETER_CUSTOM_PLUGINS_FOLDER /plugins
ENV	JMETER_BIN	${JMETER_HOME}/bin
ENV	JMETER_DOWNLOAD_URL  https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz
ENV PATH ${JMETER_BIN}:$PATH


RUN    apk update \
	&& apk upgrade \
	&& apk add ca-certificates \
	&& update-ca-certificates \
	&& apk add --update openjdk8-jre tzdata curl unzip bash \
	&& apk add --no-cache nss \
	&& rm -rf /var/cache/apk/* \
	&& mkdir -p /tmp/dependencies  \
	&& curl -L --silent ${JMETER_DOWNLOAD_URL} >  /tmp/dependencies/apache-jmeter-${JMETER_VERSION}.tgz  \
	&& mkdir -p /opt  \
	&& tar -xzf /tmp/dependencies/apache-jmeter-${JMETER_VERSION}.tgz -C /opt  \
	&& rm -rf /tmp/dependencies \
	&& apk add --no-cache busybox-extras \
	&& apk add sqlite \
	&& cp /usr/share/zoneinfo/$TZ /etc/localtime
     

ENV PATH $PATH:$JMETER_BIN


COPY ./jmeter_scripts /jmeter_scripts
COPY ./clear_table.sql ./
