FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update \
  && apt-get install wkhtmltopdf -y \
  && mv /usr/bin/wkhtmltopdf /usr/local/bin/.

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--reload"]