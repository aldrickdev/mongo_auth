src = app
version = 0.0.1
name = greymint-auth

# Runs a formatter, linter then static analyzer
:PHONY check
check: format lint 

# Builds an image for the application
:PHONY bim
bim:
	docker build -f docker/app.Dockerfile -t $(name):$(version) .

# Builds an image then runs the application 
:PHONY b-com-up
b-com-up: bim com-up

# Runs the application
:PHONY com-up
com-up:
	docker compose -f docker/compose.yaml --env-file .env up

# Runs the application in detached mode
:PHONY com-up-d
com-up-d:
	docker compose -f docker/compose.yaml --env-file .env up --detach

# Brings the application down
:PHONY com-down
com-down:
	docker compose -f docker/compose.yaml --env-file .env down


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
