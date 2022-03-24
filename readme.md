Python version: Python version >= 3.6.1 (developed using 3.8)

download requirements

```
pip install -r requirements.txt
```

start server:

```
uvicorn main:app --reload
```

run tests (Once server is not running):

```
python -m pytest tests/
```

View docs (Once the server is running):

```
http://127.0.0.1:8000/docs
```

Build Docker Container

```
docker build -f qwerty123.Dockerfile -t=qwerty-api .
```

Run Docker Container

```
docker run -d --name qwerty-api -p 8000:8000 qwerty-api
```
