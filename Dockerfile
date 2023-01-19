FROM python:3.9.7

WORKDIR /usr/src/app

#optimization: every line is a layer in the image.
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#Every time we make a change in the code, only this next line will be executed.
COPY . .

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
