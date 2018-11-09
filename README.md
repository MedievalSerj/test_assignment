# DOCUMENTS ADMIN

Test assignment.

### Requirements

1. python3.6
2. docker, docker-compose to run RabbitMQ
3. Install project requirements: `pip3 install -r requirements.txt`


### Run application

1. Launch RabbitMQ: `docker-compose up -d rabbitmq`
2. Launch celery_tasks: `celery -A celery_tasks.instance.app worker &`
3. Init db (run migrations, init roles, add default admin user): `python3 manage.py create_all`
4. Run development server: `python3 manage.py runserver`


### info

* served on: localhost:5000
* default credentials:
	- email: admin
	- password: admin
* admin user can be created with CLI: `python3 manage.py create_admin`
* regular users can be created from admin panel by the admin
