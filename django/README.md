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

## add users from command line
```
python3 manage.py createsuperuser
```

## run dev server
```
python3 manage.py runserver 0:8008
```
