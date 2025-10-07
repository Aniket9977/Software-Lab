Creating a backend using Python's FastAPI with SQLAlchemy for handling the database is a great way to meet the specified requirements. Below, I will guide you through setting up a basic FastAPI application with the necessary models, routes, and configurations as per your specifications.

### Project Setup

1. **Select runtime/framework**: Python and FastAPI.

2. **Initialize project structure and dependency management**:
    - Create a virtual environment and activate it.
    - Install required libraries:
      ```bash
      pip install fastapi[all] sqlalchemy pydantic alembic psycopg2-binary
      ```
      
3. **Configure environment variables** (e.g., create a `.env` file or use environment variables on the server):
    ```
    PORT=8000
    DATABASE_URL=sqlite:///./test.db  # Use PostgreSQL connection string for production
    ALLOWED_ORIGINS=http://localhost
    ```
 
4. **Project structure**:
   ```
   backend/
   ├── app/
   │   ├── main.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── database.py
   │   ├── routers/
   │   │   ├── contacts.py
   │   ├── services/
   │   ├── validations/
   │   ├── middlewares/
   ├── alembic/
   ├── .env
   ├── docker-compose.yml
   ├── Dockerfile
   └── requirements.txt
   ```

### Setup Database and ORM with Alembic

1. **Define your data model and create migrations**:
   
   - **`app/models.py`**:
     ```python
     from sqlalchemy import Column, String, DateTime, func
     from sqlalchemy.dialects.postgresql import UUID
     from sqlalchemy.ext.declarative import declarative_base
     import uuid

     Base = declarative_base()

     class Contact(Base):
         __tablename__ = 'contacts'
         
         id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
         name = Column(String(100), nullable=False)
         email = Column(String, nullable=False, unique=True, index=True)
         created_at = Column(DateTime(timezone=True), server_default=func.now())
         updated_at = Column(DateTime(timezone=True), onupdate=func.now())
     ```

   - **Setup Alembic**: Initialize alembic:
     ```bash
     alembic init alembic
     ```

   - **Create initial migration**:
     Configure `alembic.ini` to point to `DATABASE_URL`:
     ```ini
     sqlalchemy.url = postgresql+psycopg2://localhost/db_name
     ```

     Edit `alembic/env.py` to use the models:
     ```python
     import sys
     sys.path.append("..")
     from app.models import Base
     target_metadata = Base.metadata
     ```

     Then generate and apply the migration:
     ```bash
     alembic revision --autogenerate -m "create contacts table"
     alembic upgrade head
     ```

2. **Database connection setup**:

   - **`app/database.py`**:
     ```python
     from sqlalchemy import create_engine
     from sqlalchemy.orm import sessionmaker

     DATABASE_URL = "sqlite:///./test.db"
     engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     ```

### Create API Endpoints

1. **Define Routes**:

   - **`app/routers/contacts.py`**:
     ```python
     from fastapi import APIRouter, HTTPException, Status, Depends
     from sqlalchemy.orm import Session
     from app.models import Contact
     from app.schemas import ContactCreate, ContactResponse
     from app.database import SessionLocal
     from pydantic import BaseModel, EmailStr, constr
     
     contact_router = APIRouter()

     def get_db():
         db = SessionLocal()
         try:
             yield db
         finally:
             db.close()
     
     class ContactCreate(BaseModel):
         name: constr(min_length=1, max_length=100)
         email: EmailStr

     class ContactResponse(BaseModel):
         id: str
         name: str
         email: str
         created_at: str
     
         class Config:
             orm_mode = True

     @contact_router.post("/api/contacts", response_model=ContactResponse, status_code=201)
     async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
         db_contact = db.query(Contact).filter(Contact.email == contact.email).first()
         if db_contact:
             raise HTTPException(status_code=409, detail="duplicate_email")
         new_contact = Contact(name=contact.name.strip(), email=contact.email.lower())
         db.add(new_contact)
         db.commit()
         db.refresh(new_contact)
         return new_contact

     @contact_router.get("/api/contacts", response_model=list[ContactResponse])
     async def list_contacts(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
         contacts = db.query(Contact).offset((page - 1) * page_size).limit(page_size).all()
         return contacts
     ```

2. **Integrate routes into FastAPI**:

   - **`app/main.py`**:
     ```python
     from fastapi import FastAPI
     from fastapi.middleware.cors import CORSMiddleware
     from app.routers import contacts

     app = FastAPI(title="Contact Management System")

     app.add_middleware(
         CORSMiddleware,
         allow_origins=["*"],  # Update with ALLOWED_ORIGINS
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )

     app.include_router(contacts.contact_router)
     ```

### Additional Components and Practices

- **Validation** and **Business Rules**:
  - Ensure you validate inputs according to business rules using Pydantic models as demonstrated above.

- **Middleware and Security**:
  - Add necessary middleware such as CORS, security headers, and request size limits in `main.py`.

- ### Containerization and Deployment

1. **Dockerfile**:
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install -r requirements.txt

   COPY . .

   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **docker-compose.yml** for local development:
   ```yaml
   version: '3.7'

   services:
     db:
       image: postgres:13
       environment:
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
         POSTGRES_DB: contacts_db

     app:
       build: .
       command: uvicorn app.main:app --host 0.0.0.0 --port 8000
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       depends_on:
         - db
       environment:
         DATABASE_URL: postgres://user:password@db/contacts_db
   ```

3. **Running the Application**:
   - Run with Docker for consistency:
     ```bash
     docker-compose up --build
     ```

### Testing
- Implement unit and integration tests to ensure validation logic and endpoints work correctly.

By following these steps, you'll have a FastAPI application with a properly structured codebase, adhering to the specified requirements, incorporating database management with SQLAlchemy and Alembic, and containerization for deployment using Docker.