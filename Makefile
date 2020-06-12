BRANCH := $(shell git branch --quiet --no-color | grep '*' | sed -e 's/^\*\ //g')
HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
ash := masha
data := weather
PYTHONPATH := ${HERE}/src
TEST_PARAMS := --verbosity 2 --pythonpath "${PYTHONPATH}"
PSQL_PARAMS := --host=localhost --username=asham --password

ifeq ($(origin PIPENV_ACTIVE), undefined)
	RUN := pipenv run
endif

ifeq ($(ENV_FOR_DYNACONF), travis)
	RUN :=
	TEST_PARAMS := --failfast --keepdb --verbosity 1 --pythonpath ${PYTHONPATH}
	PSQL_PARAMS := --host=localhost --username=postgres --no-password
else ifeq ($(ENV_FOR_DYNACONF), heroku)
	RUN :=
endif

ifeq ($(origin ENV_FOR_DYNACONF), undefined)
		ENV_FOR_DYNACONF=test
endif

MANAGE := ${RUN} python src/manage.py

.PHONY: format
format:
	${RUN} isort --virtual-env ${VENV} --recursive --apply ${HERE}
	${RUN} black ${HERE}

.PHONY: sh
sh:
	${MANAGE} shell

.PHONY: psql
psql:
	psql -h localhost -U ${ash} -W -d ${data}

.PHONY: run
run: static
	 ${MANAGE} runserver 0.0.0.0:8000

.PHONY: static
static:
	${MANAGE} collectstatic --noinput --clear -v0

.PHONY: migrations
migrations:
	${MANAGE} makemigrations


.PHONY: migrate
migrate:
	${MANAGE} migrate

.PHONY: beat
beat:
	PYTHONPATH=${PYTHONPATH} \
	${RUN} celery worker \
		--app periodic.app -B \
		--config periodic.celeryconfig \
		--workdir ${HERE}/ \
		--loglevel=debug

.PHONY: su
su:
	${MANAGE} createsuperuser

.PHONY: test
test:
	ENV_FOR_DYNACONF=test \
	${RUN} coverage run \
		src/manage.py test ${TEST_PARAMS} \
				apps \
				project \

	${RUN} coverage report
	${RUN} isort --virtual-env ${VENV} --recursive --check-only ${HERE}
	${RUN} black --check ${HERE}




.PHONY: report
report:
	${RUN} coverage html --directory=${HERE}/htmlcov --fail-under=0
	open "${HERE}/htmlcov/index.html"

#.PHONY: deploy
#deploy: format test clean
#	@echo 'test branch...'
#	test "${BRANCH}" = "master"
#	@echo 'test untracked...'
#	test "${UNTRACKED}" = "0"
#	@echo 'test untracked 2...'
#	test "${UNTRACKED2}" = "0"
#	git commit --gpg-sign --signoff --message "autodeploy @ $(shell date)" --edit
#	git push origin master

.PHONY: venv
venv:
	pipenv install --dev

.PHONY: install
install:
	pipenv update --dev

.PHONY: clean
clean:
	${RUN} coverage erase
	rm -rf htmlcov
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf ./.static/

.PHONY: t
t:
	pipenv run python src/recompile_templates.py

.PHONY: resetdb
resetdb:
	psql ${PSQL_PARAMS} \
		--dbname=postgres \
		--echo-all \
		--file=${HERE}/ddl/reset_db.sql \
		--no-psqlrc \
		--no-readline \


.PHONY: initdb
initdb: resetdb migrate

.PHONY: docker
docker: wipe
	docker-compose build

.PHONY: docker-run
docker-run: docker
	docker-compose up

.PHONY: clean-docker
clean-docker:
	docker ps --quiet --all | xargs docker stop || true
	docker ps --quiet --all | xargs docker rm || true
	docker volume ls --quiet | xargs docker volume rm || true
	docker-compose rm --force || true

.PHONY: wipe
wipe: clean clean-docker
