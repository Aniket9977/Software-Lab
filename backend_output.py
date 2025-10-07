To generate a Python FastAPI backend based on the provided requirements, we'll translate these into equivalent Python steps using FastAPI and SQLAlchemy. Here's a high-level overview of how you could set up the project with corresponding features for each requirement:

### Setup and Project Configuration

1. **Project Skeleton and Dependencies**:
    - Create a new Python environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install fastapi uvicorn sqlalchemy databases alembic pydantic python-dotenv
    ```

2. **Project Structure**:
    - Basic directory structure:
    ```
    /my_fastapi_project
    ├── app
    │   ├── main.py
    │   ├── models.py
    │   ├── database.py
    │   ├── schemas.py
    │   ├── crud.py
    │   ├── routers
    │   │   ├── contacts.py
    │   └── utils.py
    ├── migrations
    ├── .env.example
    ├── alembic.ini
    ├── requirements.txt
    └── Dockerfile (optional)
    ```

### Configuration and Middleware

3. **Configuration and CORS**:
    - Use `python-dotenv` to handle environment variables.
    - Set up middleware for CORS and security headers:
    ```python
    from fastapi import FastAPI
    from starlette.middleware.cors import CORSMiddleware

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Should be restricted to frontend origin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```

### Database Setup with SQLAlchemy

4. **Database Models and ORM**:
    - Create the `models.py` file with SQLAlchemy models:
    ```python
    from sqlalchemy import Column, String, DateTime
    from sqlalchemy.dialects.postgresql import UUID
    from sqlalchemy.ext.declarative import declarative_base
    import uuid
    from datetime import datetime

    Base = declarative_base()

    class Contact(Base):
        __tablename__ = 'contacts'

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        name = Column(String, nullable=False)
        email = Column(String, unique=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)
    ```

5. **Database Connection**:
    - Setup the `database.py` file for database connectivity using databases module:
    ```python
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from databases import Database

    DATABASE_URL = "sqlite:///./test.db"  # or Postgres connection string

    database = Database(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    ```

### Migrations

6. **Setting Up Alembic for Migrations**:
    - Initialize alembic and create initial migration:
    ```bash
    alembic init migrations
    alembic revision --autogenerate -m "create contacts table"
    alembic upgrade head
    ```

### CRUD Operations

7. **CRUD Operations and Routers**:
    - Define CRUD operations in `crud.py`:
    ```python
    from sqlalchemy.orm import Session
    from . import models, schemas

    def get_contacts(db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.Contact).offset(skip).limit(limit).all()

    def create_contact(db: Session, contact: schemas.ContactCreate):
        db_contact = models.Contact(email=contact.email, name=contact.name)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    ```

    - Create FastAPI router for contacts in `routers/contacts.py`:
    ```python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from . import crud, models, schemas
    from .database import SessionLocal

    router = APIRouter()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @router.post("/contacts/", response_model=schemas.Contact)
    def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
        return crud.create_contact(db=db, contact=contact)

    @router.get("/contacts/", response_model=List[schemas.Contact])
    def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        contacts = crud.get_contacts(db, skip=skip, limit=limit)
        return contacts
    ```

### Application Initialization

8. **Initialize Application in `main.py`:**
    ```python
    from fastapi import FastAPI
    from .routers import contacts

    app = FastAPI()

    app.include_router(contacts.router, prefix="/api", tags=["contacts"])
    ```

### Optional Enhancements

9. **Security, Error Handling, and Logging**:
    - Add error handling and logging as needed.
    - Integrate rate limiting, input size restrictions.

10. **Tests**:
    - Create unit tests using pytest or unittest framework.
    - Set up a test database configuration.

11. **Documentation**:
    - Utilize FastAPI's built-in OpenAPI support for automatic docs generation.

12. **Deployment and Dockerization**:
    - Write `Dockerfile` to containerize the app.
    - Use docker-compose.yml if using Postgres.
    - Deploy to Render, Fly, or Heroku.

This scaffold will help you set up a Python FastAPI backend with SQLAlchemy, covering basic CRUD operations with `/api/contacts` and following a structure similar to what you might see in an Express-based Node.js application. Adjustments could be made based on specific project requirements and database preferences.