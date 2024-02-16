
# FastAPI Application Template

This repository hosts a FastAPI application structured to offer a familiar layout for those accustomed to Django's app-centric design. Ideal for developers looking to leverage FastAPI's asynchronous capabilities within a Django-like structure, it includes features such as JWT authentication and SQLAlchemy for ORM, with Alembic handling database migrations.

## Features

- **Django-like App Structure**: Organized for scalability and separation of concerns.
- **JWT Authentication**: Secure, token-based user authentication.
- **SQLAlchemy ORM**: Database interactions designed for asynchronous operations.
- **Alembic Database Migrations**: Easy management of database schema changes.

## Getting Started

### Prerequisites

Ensure you have the following installed before proceeding:
- Python 3.11+
- PostgreSQL (or another SQLAlchemy-compatible database)
- pip (for Python package management)

### Setup Instructions

1. **Clone the Repository**

   Start by cloning this repository to your local machine and navigate into the project directory:
   ```
   git clone https://github.com/rbtrsv/FastAPI-DjangoStructure-JWT-Alembic-SQLAlchemy.git
   cd FastAPI-DjangoStructure-JWT-Alembic-SQLAlchemy
   ```

2. **Install Dependencies**

   Install the project's required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. **Database Configuration**

   Update the `sqlalchemy.url` in `alembic.ini` to your database connection string:
   - Locate this line in `alembic.ini`:
     ```
     sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/mydatabase
     ```
   - Replace it with your actual database credentials.

### Environment Configuration

Before you can run migrations or start the application, make sure your environment is properly configured:

1. **Environment Variables**

   Optionally, set up environment variables (e.g., for database URLs, secret keys) in your environment or a `.env` file.

2. **Database Initialization**

   Use Alembic to create your database schema:
   ```
   alembic upgrade head
   ```

### Running the Application

Launch your FastAPI application with the following command:
```
uvicorn main:app --reload
```
This starts a development server at `http://127.0.0.1:8000`, with `--reload` enabling automatic reloads for development ease.

## Contributing

Your contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For substantial changes, please open an issue first to discuss what you would like to change.

## License

This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for more details.
