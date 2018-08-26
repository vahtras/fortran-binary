test:
	python -m pytest -qx test_fb.py
debug:
	python -m pytest -qx test_fb.py --pdb
coverage:
	python -m pytest -v test_fb.py --cov fortran_binary --cov-report html --cov-report term
