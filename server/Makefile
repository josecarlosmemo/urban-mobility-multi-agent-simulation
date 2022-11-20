# Makefile
venv: ## create virtual environment if venv is not present
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

requirements.txt:  venv requirements.in  ## generate requirements for release
	venv/bin/pip-compile -o requirements.txt requirements.in

dep:  ## creates a development environment, install deps
	venv/bin/pip-sync requirements.txt

run:  ## start the server
	venv/bin/python3 server.py