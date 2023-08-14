install:
	poetry install --without dev

pre-commit:
	poetry run pre-commit run --all-files

connect:
	poetry run uvicorn menu_app.main:app --reload

check:
	poetry run pre-commit run --all-files

app:
	docker-compose up -d

test:
	docker-compose -f docker-compose_test.yml up

sync-start:
	docker-compose -f docker-compose_sync.yml up

start-all:
	docker-compose up -d
	docker-compose -f docker-compose_test.yml up

stop:
	docker-compose down
	docker-compose -f docker-compose_test.yml down
	docker-compose -f docker-compose_sync.yml down


delete-images:
	docker rmi restaurant_menu-app restaurant_menu-test_app redis rabbitmq restaurant_menu-celery
