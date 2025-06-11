
add:
	bf add \
		--cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem \
		--app-id app_peevqq8j16t30s9eig000

json:
	bf app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--debug --file-type json

csv:
	bf app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--debug --file-type csv

reset:
	bf app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem --reset ./data \
		--debug

recent:
	bf app_peevqq8j16t30s9eig000 --cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem ./data \
		--date-from 2025-06-01 \
		--debug

basic:
	bf app_peevqq8j16t30s9eig000 ./data \
		--cert /etc/teller/certificate.pem \
		--cert-key /etc/teller/private_key.pem
