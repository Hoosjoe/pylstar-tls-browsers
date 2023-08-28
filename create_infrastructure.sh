#!/bin/bash

# Create directories
mkdir -p ca/root-ca/private ca/root-ca/db crl certs
chmod 700 ca/root-ca/private

# Create database
cp /dev/null ca/root-ca/db/root-ca.db
cp /dev/null ca/root-ca/db/root-ca.db.attr
echo 01 > ca/root-ca/db/root-ca.crt.srl
echo 01 > ca/root-ca/db/root-ca.crl.srl

# Create root CA request
openssl req -new -config root-ca.conf \
    -out ca/root-ca.csr \
    -keyout ca/root-ca/private/root-ca.key \
    -nodes

# Create root CA certificate (enter "y" 2 times)
printf "y\ny" | openssl ca -selfsign -config root-ca.conf \
    -in ca/root-ca.csr \
    -out ca/root-ca.crt \
    -extensions root_ca_ext

# Generate server certificate request
openssl req -new -config server.conf \
    -out certs/server.csr \
    -keyout certs/server.key \
    -nodes

# Sign the server certificate request with the root CA (enter "y" 1 time)
openssl ca -config root-ca.conf \
    -in certs/server.csr \
    -out certs/server.crt \
    -extensions server_ext
