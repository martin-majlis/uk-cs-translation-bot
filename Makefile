OPEN=xdg-open

ROOT_DIR=$(shell pwd)/
PROJECT_DIR=$(ROOT_DIR)/
TEST_DIR=$(ROOT_DIR)/tests

TRANSLATION_FILE=$(ROOT_DIR)/translation.py

TELEGRAM_DIR=$(ROOT_DIR)/telegram_uk_cs_translation_bot
TELEGRAM_PACKAGE=$(ROOT_DIR)/telegram_uk_cs_translation_bot.zip

MESSENGER_DIR=$(ROOT_DIR)/messenger_uk_cs_translation_bot
MESSENGER_PACKAGE=$(ROOT_DIR)/messenger_uk_cs_translation_bot.zip

checks: mypy test

mypy:
	mypy $(PROJECT_DIR) $(TEST_DIR)

test: test-ci

test-ci:
	pytest \
		--cov=$(PROJECT_DIR) \
		-v \
		--ignore lindat_translation_master \
		--ignore hunalign-1.1

coverage:
	coverage html -d coverage_html
	$(OPEN) coverage_html/index.html

test-and-coverage: test coverage

pre-commit-all:
	pre-commit run -a -v || git diff

pre-commit-install:
	pre-commit install

install-all: dep-install pre-commit-install

dep-install: dep-install-run dep-install-dev external-install

dep-install-run:
	pip install -r requirements.txt

dep-install-dev:
	pip install -r requirements-dev.txt

external-install:
	pip install -r $(TELEGRAM_DIR)/requirements.txt

pack-all: pack-telegram pack-messenger

pack-telegram:
	cd $(TELEGRAM_DIR); \
	rm -rfv $(TELEGRAM_PACKAGE) package; \
	echo "# COPY - DO NOT MODIFY " > t_translation.py; \
	cat $(TRANSLATION_FILE) >> t_translation.py; \
	pip install --target ./package --requirement requirements.txt; \
	cd package; \
	find . -name '__pycache__' -exec rm -rfv {} \;; \
	zip -r $(TELEGRAM_PACKAGE) .; \
	cd ..; \
	zip -g $(TELEGRAM_PACKAGE) *.py; \
	ls -l $(TELEGRAM_PACKAGE)

pack-messenger:
	cd $(MESSENGER_DIR); \
	rm -rfv $(MESSENGER_PACKAGE) package; \
	echo "# COPY - DO NOT MODIFY " > m_translation.py; \
	cat $(TRANSLATION_FILE) >> m_translation.py; \
	pip install --target ./package --requirement requirements.txt; \
	cd package; \
	find . -name '__pycache__' -exec rm -rfv {} \;; \
	zip -r $(MESSENGER_PACKAGE) .; \
	cd ..; \
	zip -g $(MESSENGER_PACKAGE) *.py; \
	ls -l $(MESSENGER_PACKAGE)
