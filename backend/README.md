# Backend

#### Create .env file in app/

```text
ACCESS_TOKEN_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
REFRESH_TOKEN_SECRET_KEY=09d22e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres_db
DATABASE_TEST_URL=postgresql://postgres:postgres@db:5432/postgres_test_db
TESTING=False
```

#### Run

    docker-compose up

#### Alembic

    docker exec -it backend alembic upgrade head
    docker exec -it backend alembic revision --autogenerate -m "some text"
