#Main App
run:
	poetry run streamlit run app.py

ruff-check:
	poetry run ruff check .

ruff-format:
	poetry run ruff format .
