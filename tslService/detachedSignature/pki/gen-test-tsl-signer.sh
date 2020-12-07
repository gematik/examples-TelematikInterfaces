#! /usr/bin/env bash

if [ ! -f test_tsl_signer_key_ecc.pem ]; then
    openssl ecparam -name brainpoolP256r1 -genkey -out test_tsl_signer_key_ecc.pem

    openssl req -x509 -key  test_tsl_signer_key_ecc.pem \
    -outform der \
    -out test_tsl_signer_ecc.der -days 365 \
    -subj "/C=DE/ST=Berlin/L=Berlin/O=gematik/OU=gematik/CN=Test TSL-Signer ECC"
else
    echo ECC Schlüssel schon vorhanden, ich erzeuge auch kein Zertifikat
fi

if [ ! -f test_tsl_signer_key_rsa.pem ]; then

    openssl genrsa 2048 >test_tsl_signer_key_rsa.pem 
    openssl req -new -x509 -key test_tsl_signer_key_rsa.pem \
      -sigopt rsa_padding_mode:pss -sha256 -sigopt rsa_pss_saltlen:32 -outform der \
      -out test_tsl_signer_rsa.der -days 365 \
      -subj "/C=DE/ST=Berlin/L=Berlin/O=gematik/OU=gematik/CN=Test TSL-Signer RSA"
else
    echo RSA-Schlüssel schon vorhanden, ich erzeuge auch kein Zertifikat
fi

