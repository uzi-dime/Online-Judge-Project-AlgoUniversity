# Online Judge

This project is an online judge system built using Django. It allows users to submit programming problems and solutions, which can then be evaluated for correctness and performance.

## Project Structure

The project consists of the following files and directories:

- `online_judge/`: The main Django application directory containing the core files.
  - `__init__.py`: Marks the directory as a Python package.
  - `asgi.py`: ASGI configuration for serving asynchronous applications.
  - `settings.py`: Configuration settings for the Django project, including database settings and installed apps.
  - `urls.py`: URL patterns mapping URLs to views.
  - `wsgi.py`: WSGI configuration for serving traditional web applications.
  
- `manage.py`: Command-line utility for interacting with the Django project.

- `pyproject.toml`: Configuration file for Poetry, specifying project dependencies and metadata.

## Installation

To set up the project, follow these steps:

1. Create a new project using Poetry:
   ```
   poetry new online-judge --src
   ```

2. Navigate into the project directory:
   ```
   cd online-judge
   ```

3. Add Django as a dependency:
   ```
   poetry add django
   ```

4. Create the Django project:
   ```
   poetry run django-admin startproject online_judge .
   ```

## Usage

To run the development server, use the following command:

```
poetry run python manage.py runserver
```

Visit `http://127.0.0.1:8080/` in your web browser to access the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.