install:
	poetry install --without dev

connect:
	poetry run uvicorn menu_app.main:app --reload

app:
	docker-compose up -d

test:
	docker-compose -f docker-compose_test.yml up -d

test-start:
	docker-compose -f docker-compose_test.yml start

start-all:
	docker-compose up -d
	docker-compose -f docker-compose_test.yml up

stop:
	docker-compose down
	docker-compose -f docker-compose_test.yml down

delete-images:
	docker rmi restaurant_menu-app restaurant_menu-test_app
