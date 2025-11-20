.PHONY: run install server clean init

init:
	uv venv .venv
	uv pip install -r requirements.txt

install:
	uv pip install -r requirements.txt

server:
	langgraph dev --host 0.0.0.0 --port 2024  --allow-blocking --no-browser

clean:
	rm -rf __pycache__ .venv
