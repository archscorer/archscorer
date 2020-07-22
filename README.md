# archscorer

Brief overview of the development enviroment. I use vanilla debian docker images
to build my development enviroment. We need:

### Run container
docker run -ti --name Archer -v $PWD:/opt/Archery:rw -p 8000-8100:8000-8100 debian

### Install node and vue
apt-get update
apt-get upgrade
apt-get install -y git-core curl build-essential openssl libssl-dev fish man-db procps python3-pip sqlite3 default-mysql-server nginx
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs
npm install -g @vue/cli

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

## Web UI for project management
Vue has web based UI that among other things lets you serve, build and lint your project.
```
cd ..
vue ui -H 0.0.0.0 -p 8000
```

However web based UI is heavier on computer than not web based UI

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

* shootoff is markerd under the type of a course. If creating new shootoff course,
  make sure to assign it correct type.
  Courses with type 's' are not used to compute sum, but its score is used for
  ordering if it is real value (not 0, null, undefined).
  In addition, it is not checked, but 'shootoff' course should appear only once
  per event.
