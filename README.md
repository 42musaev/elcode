# Backend

#### Run
    docker-compose up

#### Alembic
    docker exec -it backend alembic upgrade head
    docker exec -it backend alembic revision --autogenerate -m "some text"

Swagger <a href="http://localhost:8000/docs">docs</a>
