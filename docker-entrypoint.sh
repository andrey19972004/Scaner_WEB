#!/bin/bash


echo "======Собираем статику======"
python manage.py collectstatic --noinput

echo "======Таки ждем, пока постгра поднимется======"
while ! curl http://web_db:5432/ 2>&1 | grep '52'
do
  echo "Таки ждем....."
  sleep 1
done
echo "Таки дождались..........."

echo "======Накатываем миграции======"
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --database=API_DB

echo "======Стартуем сервер======"
python manage.py runserver 0.0.0.0:80