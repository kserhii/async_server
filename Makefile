PYTHON=python3.6

# ========== Linux (Debian) ==========


# ----- Install -----

install:
	$(if $(shell apt-cache search $(PYTHON)), , \
		sudo add-apt-repository -y ppa:fkrull/deadsnakes && apt-get update)
	sudo apt-get install -y build-essential
	sudo apt-get install -y $(PYTHON) $(PYTHON)-dev $(PYTHON)-venv cython


# ----- Virtualenv -----

venv_init:
	export XXHASH_FORCE_CFFI=1
	if [ ! -d "venv" ]; then $(PYTHON) -m venv venv ; fi;
	bash -c "source venv/bin/activate && \
		pip install --upgrade wheel pip setuptools && \
		pip install --upgrade --requirement requirements.txt"

venv_dev: venv_init
	bash -c "source venv/bin/activate && \
		pip install -r requirements-dev.txt"


# ----- Setup -----

setup: install venv_init


# ----- Update -----

update: venv_init


# ----- Clean -----

clean:
	find . -path ./venv -prune -o -name "__pycache__" -exec rm -rf {} \;
	find . -path ./venv -prune -o -name "*.pyc" -exec rm -rf {} \;
	rm -rf .cache


# ----- Remove -----

remove: clean
	rm -rf venv


# ----- Run Server -----

runserver:
	touch config/dev.yaml
	./runserver.py --config=dev
