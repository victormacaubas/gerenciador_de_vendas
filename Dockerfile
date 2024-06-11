FROM python:3.12.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN mkdir -p web/staticfiles

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN python manage.py collectstatic --noinput
WORKDIR /app/web
COPY . /app/web

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gerenciador_de_vendas.wsgi:application"]