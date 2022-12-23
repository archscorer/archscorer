# archscorer

Brief overview of the development environment. I use vanilla debian docker images
to build my development environment. You'll need:

### Run container
```
docker run -ti --name Archer -v ${PWD}:/opt/Archery:rw -p 8000-8100:8000-8100 debian
```

### Install node and vue
```
apt-get update
apt-get upgrade
apt-get install -y git-core curl build-essential openssl libssl-dev libffi-dev fish procps python3-pip mariadb-server-10.3 libmariadb-dev
curl -sL https://deb.nodesource.com/setup_16.x | bash -
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

Also need to create user and database in the database first. Then if available
import some populated database if present.

If all dependencies are there you should use docker as following:
* to start and enter container
```
docker start Archer
docker exec -ti Archer fish
```
multiple container entries are needed for convenience
start frontend (in project folder -- with package.json file)
npm ports are in `vue.config.js` file
`npm run serve`

start mysql daemon if not already running (see above)
start backend (in django folder -- with manage.py file)
`python3 manage.py runserver 0:8008`

## Legacy howto npm, yarn and vue commands

# default

## Project setup

```
# yarn
yarn

# npm
npm install

# pnpm
pnpm install
```

### Compiles and hot-reloads for development

```
# yarn
yarn dev

# npm
npm run dev

# pnpm
pnpm dev
```

### Compiles and minifies for production

```
# yarn
yarn build

# npm
npm run build

# pnpm
pnpm build
```

### Customize configuration

See [Configuration Reference](https://vitejs.dev/config/).