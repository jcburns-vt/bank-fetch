
run:
	export PYTHONPATH=src; \
	python -m fetch --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data

r:
	export PYTHONPATH=src; \
	python -m fetch --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem --reset ./data

