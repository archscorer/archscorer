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
apt-get install -y git-core curl build-essential openssl libssl-dev libffi-dev fish procps python3-pip mariadb-server-10.3 libmariadb-dev pkg-config
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

```
mysql
CREATE DATABASE my_new_database;
CREATE USER 'your_db_user'@'localhost' IDENTIFIED BY '**sequre password**';
GRANT ALL PRIVILEGES ON my_new_database.* TO 'my_new_user'@'localhost';
FLUSH PRIVILEGES;
quit
mysql -u your_db_user -p your-database_name < file.sql
```

If all dependencies are there you should use docker as following:
* to start and enter container
```
docker start Archer
docker exec -ti Archer fish
```
multiple container entries are needed for convenience
start frontend (in project folder -- with package.json file)
npm ports are in `vite.config.js` file
`npm run dev` -- to start development server
`npm run build` -- to build production version
`npm run serve` -- to preview production??

start mysql daemon if not already running (see above)
start backend (in django folder -- with manage.py file)
`python3 manage.py runserver 0:8008`
