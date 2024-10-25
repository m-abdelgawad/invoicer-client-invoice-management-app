FROM python:3.10

RUN apt-get update

RUN apt-get install -y netcat-openbsd

RUN useradd --system --create-home --shell=/bin/bash --uid=1000 appuser

WORKDIR /invoicer

# Copy only the requirements file first
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8000

RUN chown -R appuser:appuser /invoicer
RUN chmod +x entrypoint.sh

USER appuser
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["bash", "entrypoint.sh"]