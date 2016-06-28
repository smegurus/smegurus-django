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
  git clone git@gitlab.cloudmasterstudios.com:smegurus/django-bizmula.git
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

5. **OS X** USERS ONLY: (a) Check what Postgres.app version you are using. (b) For Postgres we need the following $PATH, so just type it in.

  ```bash
  export PATH="/Applications/Postgres.app/Contents/Versions/9.5/bin:$PATH"
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
  drop database bizmula_db;
  create database bizmula_db;
  CREATE USER django WITH PASSWORD NULL;
  GRANT ALL PRIVILEGES ON DATABASE bizmula_db to django;
  ALTER USER django CREATEDB;
  ```

  **Linux / FreeBSD**

  ```sql
  /usr/local/bin/dropdb bizmula_db;
  /usr/local/bin/createdb bizmula_db;
  /usr/local/bin/psql bizmula_db;
  CREATE USER django WITH PASSWORD NULL;
  GRANT ALL PRIVILEGES ON DATABASE bizmula_db to django;
  ALTER USER django CREATEDB;
  ```

9. Copy our sample .env file to be our new file and open it up:

  ```bash
  cp ~/django-bizmula/bizmula/dotenv_sample ~/django-bizmula/bizmula/.env
  vi ~/django-bizmula/bizmula/.env
  ```

10. While inside the ``.env`` file, please fill it to match your configuration.

11. Setup the database.

  ```bash
  python manage.py makemigrations;
  python manage.py migrate_schemas
  python manage.py setup_tenants
  ```

12. Setup your **root** user.

  ```bash
  python manage.py createsuperuser;
  ```

### Usage
#### Running Development
If you are developing locally from your machine, use this command.

```bash
python manage.py runserver
```

#### Running Production
If you plan on running a more rugged server that utilizes your installed instance of ``nginx`` then run this command.

```bash
gunicorn -c gunicorn_config.py bizmula.wsgi
```

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

In your browser, load up: ```http://bizmula.com```.

#### Setup Domain on OS X
1. Go to ``hosts`` file

  ```bash
  sudo vi /etc/hosts
  ```

2. Add the following:

  ```bash
  127.0.0.1  bizmula.com
  127.0.0.1  www.bizmula.com
  ```

3. Restart the DNS:

  ```bash
  dscacheutil -flushcache
  ```

4. To run the server:

  ```bash
  sudo python manage.py runserver bizmula.com:80
  ```
