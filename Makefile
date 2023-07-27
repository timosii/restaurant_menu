install:
	poetry install

uvicorn-connect:
	poetry run uvicorn menu_app.main:app --reload
