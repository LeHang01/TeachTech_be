FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=be_teachtech.settings

# Copy the entire project into the container
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for the Django app
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
