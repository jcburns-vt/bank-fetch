
run:
	export PYTHONPATH=src; \
	python -m fetch --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data

reset:
	export PYTHONPATH=src; \
	python -m fetch --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem --reset ./data

recent:
	export PYTHONPATH=src; \
	python -m fetch --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--date-from 2025-06-01

