FROM python:3

WORKDIR /usr/src/app

#COPY requirements.txt ./
RUN pip install --no-cache-dir django -i https://pypi.douban.com/simple

COPY . .

CMD [ "python", "./manage.py","runserver"]
