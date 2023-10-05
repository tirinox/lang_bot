include .env
export

.DEFAULT_GOAL := help
.PHONY: build start stop restart pull logs clean upgrade redis-cli redis-sv-loc test lint

BOTNAME = lang_tg_bot

help:
	@echo "Available targets:"
	@python3 -c "import os; f = open('Makefile'); print(' | '.join(line.strip()[:-1] for line in f.readlines() if line.strip().endswith(':'))); f.close()"


build:
	$(info Make: Building images.)
	docker-compose build --no-cache $(BOTNAME)
	echo "Note! Use 'make start' to make the changes take effect (recreate containers with updated images)."

start:
	$(info Make: Starting containers.)
	@docker-compose up -d
	$(info Wait a little bit...)
	@sleep 3
	@docker ps

stop:
	$(info Make: Stopping containers.)
	@docker-compose stop

restart:
	$(info Make: Restarting containers.)
	@make -s stop
	@make -s start

poke:
	@docker-compose restart $(BOTNAME)
	@make -s logs

pull:
	@git pull

logs:
	@docker-compose logs -f --tail 1000 $(BOTNAME)

clean:
	@docker system prune --volumes --force

upgrade:
	@make -s pull
	@make -s build
	@make -s start

redis-cli:
	@redis-cli -p $(REDIS_PORT) -a $(REDIS_PASSWORD)

redis-sv-loc:
	cd redis_data
	redis-server

test:
	cd src && python -m pytest tests

lint:
	find ./src/ -type f -name "*.py" | xargs pylint
