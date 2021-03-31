.PHONY: install-tests coverage

install-tests:
	pip install -e '.[tests]'

coverage:
	pytest --cov --cov-context=test
	coverage html --show-contexts
	coverage report --skip-covered --fail-under 100
