src = app
version = 0.0.1
name = user_auth

:PHONY check
check: lint format stana

:PHONY bim
bim:
	docker build -f docker/Dockerfile -t $(name):$(version) .

:PHONY runcon
runcon:
	docker run --rm -it --name $(name) $(name):$(version)

# Helpers

:PHONY format
format:
	black $(src)

:PHONY lint
lint:
	flake8 $(src)

:PHONY stana
stana:
	mypy $(src)
