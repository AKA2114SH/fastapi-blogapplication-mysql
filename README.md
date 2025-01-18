# FastAPI Blog Application with MySQL

A comprehensive RESTful API blog application built with FastAPI and MySQL, featuring user authentication, blog post management, and secure data handling.

## Features

- 🔐 JWT Authentication
- 📝 Blog Post CRUD Operations
- 🗄️ MySQL Database Integration
- 🚀 FastAPI Framework
- 🔄 RESTful API Architecture
- 🛡️ Secure Password Hashing

## Tech Stack

- **FastAPI**: Modern Python web framework for building APIs
- **MySQL**: Relational database for persistent storage
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PyJWT**: JSON Web Token implementation
- **Python 3.8+**: Core programming language

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AKA2114SH/fastapi-blogapplication-mysql.git
cd fastapi-blogapplication-mysql
```

2. Create a virtual environment:
```bash
python -m venv .vscode
source .vscode/bin/activate  # On Windows: .vscode\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your MySQL database in `database.py`

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication
- POST `/auth/register`: Register new user
- POST `/auth/login`: Login user

### Blog Posts
- GET `/posts`: Get all blog posts
- GET `/posts/{id}`: Get specific blog post
- POST `/posts`: Create new blog post
- PUT `/posts/{id}`: Update blog post
- DELETE `/posts/{id}`: Delete blog post

## Project Structure

```
fastapi-blogapplication-mysql/
├── alembic/              # Database migrations
├── blog/                 # Blog related modules
├── .vscode/              # Virtual environment
├── main.py              # Application entry point
├── database.py          # Database configuration
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Development

The project uses Alembic for database migrations and SQLAlchemy as the ORM. The authentication system is implemented using JWT tokens for secure user sessions.

### Database Configuration

Update the database connection string in `database.py`:

```python
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/dbname"
```

### Running Tests

To run the test suite:

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Python community

## Contact

Your Name - [@AKA2114SH](https://github.com/AKA2114SH)

Project Link: [https://github.com/AKA2114SH/fastapi-blogapplication-mysql](https://github.com/AKA2114SH/fastapi-blogapplication-mysql)
