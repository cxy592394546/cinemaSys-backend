FROM python:3.6
WORKDIR /root/Project/demo

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "demo:app", "-c", "./gunicorn.conf.py"]