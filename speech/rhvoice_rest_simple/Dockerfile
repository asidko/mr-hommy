FROM ubuntu:18.04
# Install libs
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get update && apt-get install -y tzdata unzip git scons build-essential libxml2 libxslt-dev python3-lxml python-lxml libao4 libao-dev pkg-config libpulse-dev flite1-dev libao-dev portaudio19-dev lame python3 python3-pip python3-setuptools locales locales-all
RUN pip3 install flask pymorphy2

# Install RHVoice
# Install from zip archive (contains English, Russian, Ukrainian languages only)
ADD RHVoice*.zip /opt/RHVoice/
RUN unzip /opt/RHVoice/RHVoice*.zip -d /opt/RHVoice && rm -rf /opt/RHVoice/RHVoice*.zip && \
    cd /opt/RHVoice/RHVoice* && scons && scons install && ldconfig
# Install from git - comment "Install from archive" and uncomment this section
#RUN git clone --depth=1 --branch 1.2.3 https://github.com/Olga-Yakovleva/RHVoice.git /opt/RHVoice && \
#    cd /opt/RHVoice && scons && scons install && ldconfig

# Cleanup
RUN cd /opt && rm -rf /opt/RHVoice && \
    apt-get purge -y build-essential scons pkg-config libxml2 libxslt-dev python3-lxml python-lxml binutils bzip2 cpp cpp-5 dpkg-dev g++ g++-5 gcc gcc-5 libdpkg-perl libgcc-5-dev libstdc++-5-dev make uuid-dev

# Add dictionary
# Russian dictionary
ADD dicts/Russian/*.* /usr/local/etc/RHVoice/dicts/Russian/
# Ukrainian dictionary
ADD dicts/Ukrainian/*.* /usr/local/etc/RHVoice/dicts/Ukrainian/

ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8

ADD app.py /opt/app.py

EXPOSE 8080/tcp

VOLUME ["/usr/local/etc/RHVoice"]

CMD python3 /opt/app.py
