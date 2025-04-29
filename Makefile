IMAGE:=aaa-frontend

help:
	@echo "help - show this help"
	@echo "build - build docker image"
	@echo "test - run tests"
	@echo "lint - run lining"
	@echo "run - start applicaion"
	@echo "dev - start applicaion in dev mode with live reload"

clean:
	@docker rmi -f ${IMAGE}

build:
	@docker build -t ${IMAGE} . --network=host

dev: build
@docker run --rm -v $(PWD):/app \
		-v $(PWD)/mlruns:/app/mlruns \
		-p 0.0.0.0:8000:8000 \
		-p 0.0.0.0:8001:8001 \
		-it ${IMAGE} \
		adev runserver --livereload --host 0.0.0.0 --port 8000 run.py

run: build
	@docker run --rm -it \
		-v $(PWD)/mlruns:/app/mlruns \
		-p 0.0.0.0:8000:8000 ${IMAGE}

test: build
	@echo 'Run tests'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pytest --disable-warnings -v

flake8: build
	@echo 'Run flake8'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m flake8 lib

pycodestyle: build
	@echo 'Run pycodestyle'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pycodestyle lib

pylint: build
	@echo 'Run pylint'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pylint lib

black: build
	@echo 'Run black'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m black lib

lint: black flake8 pycodestyle pylint

mlflow-ui:
	@echo 'Starting MLflow UI'
	mlflow ui --backend-store-uri ./mlruns --host 0.0.0.0 --port 5001