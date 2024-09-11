#!/bin/bash

# Generate a 2048-bit RSA private key
openssl genrsa -out dummy.key 2048

# Generate a self-signed certificate
openssl req -x509 -new -nodes -key dummy.key -sha256 -days 1024 -out dummy.crt -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=example.com"

# Display the certificate
echo "Dummy Certificate:"
openssl x509 -in dummy.crt -text -noout

# Display the private key
echo "Dummy Private Key:"
cat dummy.key