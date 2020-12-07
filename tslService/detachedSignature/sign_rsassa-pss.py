#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives import serialization

from binascii import unhexlify
from struct import pack

(tsl_signer_cert, tsl_dtbs, serialized_private_key ) = [ 
    open(filename, "rb").read() for filename in [ 
        "pki/test_tsl_signer_rsa.der", "TSL-dummy.xml", "pki/test_tsl_signer_key_rsa.pem" ] ]

private_key = serialization.load_pem_private_key(serialized_private_key, password=None, backend=default_backend())
signature = private_key.sign(tsl_dtbs, padding.PSS(
                          mgf=padding.MGF1(hashes.SHA256()),
                          salt_length=32 #salt_length=padding.PSS.MAX_LENGTH
                          ), hashes.SHA256())

#signature = unhexlify("0382") + pack("h", len(signature))[::-1]
signature = unhexlify("0382010100") + signature

pre_output = unhexlify(\
"""
303d 0609 2a86 4886 f70d 0101 0a30 30a0
0d30 0b06 0960 8648 0165 0304 0201 a11a
3018 0609 2a86 4886 f70d 0101 0830 0b06
0960 8648 0165 0304 0201 a203 0201 20  
""".replace("\n","").replace(" ","")) + \
             signature + \
             tsl_signer_cert

output = unhexlify("3082") + pack("h", len(pre_output))[::-1] + pre_output 

with open("TSL-dummy.sig", "wb") as f:
    f.write(output)

