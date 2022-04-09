ifeq ($(env), dev)
	compose_options := -p pay_sys_dev -f docker-compose.yaml -f docker-compose.dev.yaml
else
	compose_options := -p pay_sys -f docker-compose.yaml
endif

ifeq ($(s),)
	service := payment_gateway
else
	service := $(s)
endif


init:
	cp -n config/.env.tmpl config/.env

build:
	docker-compose $(compose_options) build $(options)

up:
	docker-compose $(compose_options) up -d
	docker-compose $(compose_options) logs --tail=100 -f
logs:
	docker-compose $(compose_options) logs --tail=100 -f
down:
	docker-compose $(compose_options) down
shell:
	docker-compose $(compose_options) exec $(service) /bin/bash
