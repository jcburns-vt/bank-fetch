

json:
	export PYTHONPATH=src; \
	python -m fetch app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--debug --file-type json

csv:
	export PYTHONPATH=src; \
	python -m fetch app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--debug --file-type csv

reset:
	export PYTHONPATH=src; \
	python -m fetch app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem --reset ./data \
		--debug

recent:
	export PYTHONPATH=src; \
	python -m fetch app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--date-from 2025-06-01 \
		--debug

