# pull official base image
FROM python:3.10.4-slim

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# add app
COPY . .

# start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
