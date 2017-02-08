# Bizmula Django App
## Introduction
A cloud-based application used to help entrepreneurs throughout the lifecycle of their businesses.

## Minimum Requirements
* Python 3.4
* Postgres 9.4
* pip 8.1
* virtualenv 15.0.0

## Instructions
### Setup
1. Clone the projects.

  ```bash
  git clone git@gitlab.cloudmasterstudios.com:smegurus/smegurus-django.git
  ```

2. Init the virtual environment.

  **OS X**

  ```bash
  python3 -m venv env
  ```

  **Linux / FreeBSD**

  ```bash
  virtualenv env
  ```

3. Now lets activate virtualenv

  ```bash
  source env/bin/activate
  ```

4. Confirm we are using Python3

  ```bash
  python --version  # Should return Python 3.4+
  ```

5. **OS X** USERS ONLY: (a) Check what Postgres.app version you are using. (b) For Postgres we need the following $PATH, so just type it in. If you have a different version installed, please change it the `9.6` version to your current version.

  ```bash
  export PATH="/Applications/Postgres.app/Contents/Versions/9.6/bin:$PATH"
  ```

6. Install the required Python libraries.

  **Automatically**

  *Note: Please use this method of installation.*

  ```bash
  pip install -r requirements.txt
  ```

  **Manually**

  *Note: Use this method if your automatic installation breaks and you need to diagnose the problem.*
  See: requirements.txt

7. Load up ``pgsql`` console.

  ```bash
  (OS X)
  (Click Applications and click "postgres" icon)

  (Linux / FreeBSD)
  su pgsql
  ```

8. Once in the ``pgsql`` console, write the following commands:

  **OS X**

  ```sql
  drop database smegurus_db;
  create database smegurus_db;
  \c smegurus_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE smegurus_db to django;
  ALTER USER django CREATEDB;
  ALTER ROLE django SUPERUSER;
  CREATE EXTENSION postgis;
  ```

  **Linux / FreeBSD**

  ```sql
  sudo -i -u postgres
  psql

  DROP DATABASE smegurus_db;
  CREATE DATABASE smegurus_db;
  \c smegurus_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE smegurus_db to django;
  ALTER USER django CREATEDB;
  -- ALTER ROLE django SUPERUSER;
  CREATE EXTENSION postgis;
  ```

9. Copy our sample .env file to be our new file and open it up:

  ```bash
  touch ~/smegurus-django/smegurus/.env
  vi ~/smegurus-django/smegurus/.env
  ```

10. While inside the ``.env`` file, please fill it to match your configuration.

11. Setup the database.

  ```bash
  python manage.py makemigrations;
  python manage.py migrate;
  python manage.py migrate_schemas
  python manage.py populate_public
  python manage.py setup_fixtures
  ```

12. Setup your **root** user.

  ```bash
  python manage.py createsuperuser;
  ```

#### Celery
##### MacOS

1. Install `redis`.
  ```bash
  brew install redis
  ```

2. Afterwords lets get it started.
  ```
  brew services start redis
  ```

3. Confirm it is working by running the following command waiting to get a ``PONG`` response:
  ```
  redis-cli ping
  ```

4. Congratulations you are now setup.

5. Addendum - Running this command will force ``redis`` to load up everytime your computer starts up.
  ```
  ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
  ```

6. Addendum - Running this command will stop ``redis`` from loading up every time your computer starts up.
  ```
  launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
  ```

#### Setup Domain on OS X
1. Go to ``hosts`` file
  ```bash
  sudo vi /etc/hosts
  ```

2. Add the following:
  ```bash
  127.0.0.1  smegurus.co
  127.0.0.1  www.smegurus.co
  ```

3. Restart the DNS:
  ```bash
  dscacheutil -flushcache
  ```


### Usage
#### Running Development
Before you run the application, you need to load up celery in a separate console terminal:
  ```bash
  celery -A smegurus worker -l info;
  ````


If you are developing locally from your machine, use this command.
  ```bash
  sudo python manage.py runserver smegurus.co:80;
  ```

Notes:
- When it asks for your password, use your MacOS password.


#### Running Unit Tests
##### Run All App Tests
This command will run all the unit tests our application has:

```bash
python manage.py test
```

##### Run Specific App Tests
If you want to run all the unit tests for a particular app. Run the following:

```bash
python manage.py test api.tests
```

##### Run Specific Tests within an App
There are cases where an application may have countless unit tests and you want to run a particular set. Run the following:

```bash
python manage.py test api.tests.test_authentication
```

#### Viewing Web-Application

In your browser, load up: ```http://smegurus.co```.
