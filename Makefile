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
	docker-compose $(compose_options) up -d payment_gateway_db
	docker-compose $(compose_options) exec payment_gateway_db sh -c "until pg_isready -U postgres -d payment_gateway_db; do sleep 1; done"
	docker-compose $(compose_options) up -d payment_gateway
	docker-compose $(compose_options) exec payment_gateway sh -c "alembic upgrade head"
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


auth-init:
	cp -n config/.env.auth.tmpl config/.env.auth
auth-up:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml up
# 	docker-compose -p auth_graduate -f docker-compose.auth.yaml up -d
# 	docker-compose -p auth_graduate -f docker-compose.auth.yaml logs --tail=100 -f
auth-down:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml down
auth-build:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml build auth_api
auth-logs:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml logs --tail=100 -f
auth-shell:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml exec $(service) /bin/bash
