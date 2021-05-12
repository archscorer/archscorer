# archscorer

Brief overview of the development enviroment. I use vanilla debian docker images
to build my development enviroment. You'll need:

### Run container
```
docker run -ti --name Archer -v ${PWD}:/opt/Archery:rw -p 8000-8100:8000-8100 debian
```

### Install node and vue
```
apt-get update
apt-get upgrade
apt-get install -y git-core curl build-essential openssl libssl-dev libffi-dev fish procps python3-pip mariadb-server-10.3 libmariadb-dev
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs
npm install -g @vue/cli
```
* running mysql in docker takes few more steps
```
mkdir /run/mysqld
chmod 777 /run/mysqld
mysqld &
mysql_secure_installation
```

If all dependencies are there you should use docker as following:
* to start and enter container
```
docker start Archer
docker exec -ti Archer fish
```
multiple container entries are need for convenience
start frontend (in project folder -- with package.json file)
npm ports are in `vue.config.js` file
`npm run serve`

start backend (in django folder -- with manage.py file)
`python3 manage.py runserver 0:8008`

## Legacy howto npm and vue commands

### Web UI for project management
Vue has web based UI that among other things lets you serve, build and lint your project.
```
cd ..
vue ui -H 0.0.0.0 -p 8000
```

However web based UI is heavier on computer than not web based UI

### List of commands that are otherwise useful

#### Project setup
```
npm install
```

#### Compiles and hot-reloads for development
```
npm run serve
```

#### Compiles and minifies for production
```
npm run build
```

#### Lints and fixes files
```
npm run lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
