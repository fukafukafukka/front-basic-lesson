FROM python:3.8
USER root
# 自分の環境のマウントするディレクトリを書いてください。なおdocker run時に「-v」でマウントする必要有り。
WORKDIR /Users/fukazawakeisuke/lesson/spotify
RUN apt-get update
RUN apt-get install -y \
vim \
git \
locales
# 他に欲しいライブラリあったらここに追記して使ってください
RUN pip3 install requests numpy pandas spotify
RUN locale-gen ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
