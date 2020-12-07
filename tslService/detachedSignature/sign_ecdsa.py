#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from binascii import unhexlify
from struct import pack

with open("pki/test_tsl_signer_ecc.der", "rb") as f:
    tsl_signer_cert = f.read()

with open("ECC-RSA_TSL-dummy.xml", "rb") as f:
    tsl_dtbs = f.read()

with open("pki/test_tsl_signer_key_ecc.pem", "rb") as f:
    serialized_private_key = f.read()

private_key = serialization.load_pem_private_key(serialized_private_key,
                            password=None, backend=default_backend())
signature = private_key.sign(tsl_dtbs, ec.ECDSA(hashes.SHA256()))

pre_output = unhexlify("30 0A 06 08 2A 86 48 CE 3D 04 03 02".replace(" ","")) + \
             signature + \
             tsl_signer_cert

output = unhexlify("3082") + pack("h", len(pre_output))[::-1] + pre_output 

with open("ECC-RSA_TSL-dummy.sig", "wb") as f:
    f.write(output)

