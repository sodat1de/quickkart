dev:
	docker compose up --build

test:
	docker compose run --rm user-svc pytest
	docker compose run --rm product-svc pytest
	docker compose run --rm order-svc pytest