setup:
	poetry export -f requirements.txt --output requirements.txt

init:
	python -m venv venv/
	venv/bin/pip install -r requirements.txt
	venv/bin/python melhorenvio -p

import:
	venv/bin/python melhorenvio -l=logs.txt

report:
	venv/bin/python melhorenvio -r=report.csv