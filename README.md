# archscorer

## Web UI for project management
Vue has web based UI that among other things lets you serve, build and lint your project.
```
cd ..
vue ui -H 0.0.0.0 -p 8000
```

However web based UI is heavier on computer than not web based UI

Brief overview of the development enviroment. I use vanilla debian docker images
to build my development enviroment. We need:
* python3
* npm
* mysql

If all dependencies are there you should use docker as following:
* to start and enter container
```
docker start Archer
docker exec -ti Archer fish
```
multiple container entries are need for convenience
start frontend (in project folder -- with package.json file)
npm ports are in `vue.config.js` file
`npm run serve --watch`

start backend (in django folder -- with manage.py file)
`python3 manage.py runserver 0:8008`


## List of commands that are otherwise useful

### Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Documentation snippets

* shootoff is currently set up so, that from rounds we look courses, that name
 contains word 'shootoff'. If such appears, it is not used to compute sum, but
 its score is used for ordering if it is real value (not 0, null, undefined).


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
