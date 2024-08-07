# Testing

We have a basic testing setup in place that covers database insertion and API retrieval.

The tests are located inside the `src/tests` directory and can be executed using the following command:

```bash
pipenv run pytest
#or
pytest
```

We also have a GitHub test workflow set up in `test.yml` that runs on every pull request and merge on the main branch to ensure that the tests are passing.

## Adding new Tests

New tests can also be added to the folder `src/tests`.

The files must be prefixed with `test_` for pytest to recognize them.

A testing function should also be created with the prefix `test_`.

eg:

```python
def test_create_get_task_integration():
    assert 1+1=2
```

We use dependency overriding of Repositories with different databases to ensure that they do not interfere with your actual database. The dependencies can be overridden as shown below.

```python

from app import app


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


db_models.BaseModel.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_task_repository(session: Session = Depends(override_get_db)):
    return TaskRepository(session)

app.dependency_overrides[get_task_repository] = override_get_task_repository

```

For a comprehensive guide on testing with FastAPI, please refer to the [FASTAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) documentation.

Note:
It is always challenging to perform integration testing, especially when dealing with LLMS and queues. However, the API endpoints have been thoroughly tested to ensure accurate responses.
