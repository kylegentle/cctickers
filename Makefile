init:
	pip install pipenv
	pipenv install

ci:
	pipenv run pytest --cov=cctickers
