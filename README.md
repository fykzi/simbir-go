Для запуска понадобится установить Docker и Docker-compose

Linux
1. docker-compose up
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. alembic upgrade heads
6. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## URL: http://0.0.0.0:8000/
