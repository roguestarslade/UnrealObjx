VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

build-deps: deps
	$(PYTHON) build_index.py

deps:
	@if [ ! -f "$(PIP)" ]; then \
		echo "🔧 Creating virtualenv..."; \
		python3 -m venv $(VENV_DIR); \
	fi && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt
