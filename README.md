# rssreader

Install all the packages from requirements.txt 
Using this command pip install -r requirements.txt

Run command: python manage.py makemigrations
Run command: python manage.py migrate

Run command: python manage.py runserver

to update feeds we need run celery task every 1 hour
So i have used django-celery-beat. We need to set periodic Task using admin panel.
