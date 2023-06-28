# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.11
FROM python:3.11

WORKDIR /app

# Copy the entire project directory to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Set the entry point to run the utility
CMD ["python", "run_address_book.py"]