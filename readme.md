Python version: Python version >= 3.6

download requirements

```
pip install -r requirements.txt
```

start server:

```
uvicorn main:app --reload
```

run tests:

```
python -m pytest tests/
```

View docs (Once the server is running):

```
http://127.0.0.1:8000/docs
```
