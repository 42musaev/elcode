while ! nc -z db 5432; do sleep 1; done;
alembic upgrade head
echo "-------------------------> http://0.0.0.0:8000/api/v1/docs <-------------------------"
uvicorn app.main:app --host 0.0.0.0 --reload
