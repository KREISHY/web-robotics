start-venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

db-start:
	docker compose up -d postgres

db-drop:
	docker compose rm -sf postgres
	docker volume rm -f test_api_data

clean-up:
	docker system prune
	docker volume prune
	docker volume rm $(docker volume ls -qf dangling=true)

migrate:
	venv/bin/python3 src/manage.py makemigrations users competitions
	venv/bin/python3 src/manage.py migrate

entry-point:
	export DJANGO_SETTINGS_MODULE=project.settings && venv/bin/python3 src/entrypoint.py

build: start-venv migrate entry-point
