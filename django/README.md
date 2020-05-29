# archscorer

## Project setup
```
django-admin startproject db_api
```

## Create app
```
python3 manage.py startapp archscorer
```

## migrations [to do every time database model classes are changed]
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## add users from command line [needed only once, upon creation of the database]
```
python3 manage.py createsuperuser
```

## run dev server [this is the main operation needed for development]
```
python3 manage.py runserver 0:8008
```

# Setting up new instance
```
python3 manage.py loaddata initdata
```
This needs to be still added by https://docs.djangoproject.com/en/2.2/howto/initial-data/
