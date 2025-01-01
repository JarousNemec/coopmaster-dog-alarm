FROM  ultralytics/ultralytics:8.3.3-python

RUN mkdir build

WORKDIR /build

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9008


CMD [ "python", "/build/main.py"]
