.PHONY: test run

test:
	pytest -q

run:
	uvicorn backend.app.main:app --reload
