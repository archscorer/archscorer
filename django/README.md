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

#### Update sequence in server (could be script?)

First backup sql database
```
mysqldump --databases {db} > {db.sql}
```

```
# in repo folder
git pull
cd django/
./manage.py migrate
cd public/
rm index.html
cp ../frontend/index.html .
cd static/
rm -r js/ css/
cp -r ../../frontend/static/js ../../frontend/static/css .
cd ../..
touch tmp/restart.txt
```
