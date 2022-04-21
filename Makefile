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
	docker-compose -p auth_graduate -f docker-compose.auth.yaml up -d postgres
	docker-compose -p auth_graduate -f docker-compose.auth.yaml exec postgres sh -c "until pg_isready -U postgres -d movies; do sleep 1; done"
	docker-compose -p auth_graduate -f docker-compose.auth.yaml up -d auth_api
	docker-compose -p auth_graduate -f docker-compose.auth.yaml exec auth_api sh -c "alembic upgrade head"
	docker-compose -p auth_graduate -f docker-compose.auth.yaml exec postgres sh -c "psql -U postgres movies -c \"INSERT INTO products (id, product_name, cost, currency) VALUES ('8b14aa60-6b09-4ced-a344-aca486419592', 'Subscription, 1 month', 10, 'USD');\""
auth-up:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml up -d
	docker-compose -p auth_graduate -f docker-compose.auth.yaml logs --tail=100 -f
auth-down:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml down
auth-build:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml build auth_api
auth-logs:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml logs --tail=100 -f
auth-shell:
	docker-compose -p auth_graduate -f docker-compose.auth.yaml exec $(service) /bin/bash
