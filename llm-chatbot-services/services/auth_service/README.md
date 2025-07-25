# Auth Service

The Auth Service is a core component of the LLM Chatbot Platform, responsible for managing user authentication, authorization, and related functionalities. It provides a secure and reliable way to handle user registration, login, token management, and password recovery.

## Features

- **User Registration:** Allows new users to create an account.
- **User Login:** Authenticates users and provides JWT access and refresh tokens.
- **Token-Based Authentication:** Secures endpoints using JSON Web Tokens (JWT).
- **Token Refresh:** Enables users to obtain a new access token using a refresh token without re-entering their credentials.
- **Role-Based Access Control (RBAC):** Restricts access to certain endpoints based on user roles (e.g., `admin`, `user`).
- **Password Management:** Includes functionality for password hashing, verification, and a secure password reset mechanism.
- **Logout:** Provides a way to invalidate refresh tokens, effectively logging users out.

## [Swagger](https://github.com/Swayam595/LLM-Chatbot-Microservice-Platform/blob/main/project-documentation/service-documentation/auth-service/openai.json)

## API Endpoints

The service exposes the following RESTful API endpoints:

| Method | Path                | Description                                                                                                                               |
|--------|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `GET`  | `/`                 | A welcome endpoint to confirm that the service is running.                                                                                |
| `GET`  | `/health`           | A health check endpoint to monitor the service's status.                                                                                  |
| `POST` | `/register`         | Registers a new user with a unique email and a hashed password.                                                                           |
| `POST` | `/login`            | Authenticates a user and returns JWT access and refresh tokens upon successful validation.                                                |
| `POST` | `/logout`           | Invalidates the user's refresh token, requiring them to log in again to get a new one.                                                    |
| `POST` | `/refresh`          | Issues a new access token if the provided refresh token is valid.                                                                         |
| `POST` | `/forgot-password`  | Sends a password reset token to the user's registered email address.                                                                      |
| `POST` | `/reset-password`   | Allows a user to reset their password using a valid reset token.                                                                          |
| `GET`  | `/me`               | A protected endpoint that returns the profile of the currently authenticated user.                                                        |
| `GET`  | `/admin-only`       | A protected endpoint accessible only to users with the `admin` role.                                                                      |

---

## Project Structure

The `auth_service` follows a structured and modular design to separate concerns and enhance maintainability. Below is a high-level overview of the key directories and their responsibilities:

- **`app/`**: The main application directory.
  - **`dependencies/`**: Contains dependency injection functions for authentication, authorization, and repository access.
  - **`models/`**: Defines the SQLAlchemy database models (`User`, `RefreshToken`).
  - **`repositories/`**: Manages data access logic, interacting with the database through repositories (`UserRepository`, `RefreshTokenRepository`).
  - **`schemas/`**: Defines the Pydantic data validation schemas for API requests and responses.
  - **`services/`**: Contains the core business logic for user management, authentication, and password services.
  - **`main.py`**: The entry point of the FastAPI application, where all endpoints are defined.
- **`config/`**: Manages application configuration, including database settings and JWT secrets.
- **`tests/`**: Contains unit and integration tests for the service.
- **`Dockerfile`**: Defines the containerization setup for the service.
- **`pyproject.toml`**: Manages project dependencies and metadata.
- **`README.md`**: This file, providing an overview and documentation for the service.

This structure ensures that each component has a clear responsibility, making the codebase easier to understand, test, and scale.
