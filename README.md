# Email and OTP Service

This is a Django-based mail microservice that handles sending OTPs for verification and sending emails. It is designed to be integrated with other microservices, for various task purposes.

## Features

- Send OTPs to users via email.
- Verify OTPs sent to users.
- Send general emails.
- Swagger documentation for all endpoints.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST framework
- drf-yasg (for Swagger documentation)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/email-service.git
    cd mail
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure the email settings in `mail/settings.py`:

    ```python
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your_email@example.com'
    EMAIL_HOST_PASSWORD = 'your_email_password'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ```

5. Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver 0.0.0.0:8594
    ```

## Endpoints

### Send OTP

- **URL:** `/service/send-otp/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "email": "user@example.com"
    }
    ```
- **Response:**
    - `200 OK` if the OTP is sent successfully.
    - `400 Bad Request` if there is an error in the request.

### Verify OTP

- **URL:** `/service/verify-otp/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "otp": "123456"
    }
    ```
- **Response:**
    - `200 OK` if the OTP is verified successfully.
    - `400 Bad Request` if the OTP is invalid or expired.

### Send Email

- **URL:** `/service/send-email/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "to_email": "user@example.com",
        "subject": "Email Subject",
        "message": "Email message content."
    }
    ```
- **Response:**
    - `200 OK` if the email is sent successfully.
    - `400 Bad Request` if there is an error in the request.

## Swagger Documentation

The Swagger UI for API documentation is available at:

- Swagger UI: [http://localhost:8594/swagger/](http://localhost:8594/swagger/)
- ReDoc: [http://localhost:8594/redoc/](http://localhost:8594/redoc/)
