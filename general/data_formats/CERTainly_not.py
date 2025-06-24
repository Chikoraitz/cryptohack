"""
######
PEM is just a nice wrapper above DER encoded ASN.1. 
In some cases you may come across DER files directly; for instance 
many Windows utilities prefer to work with DER files by default. 
However, other tools expect PEM format and have difficulty importing 
a DER file, so it's good to know how to convert one format to another.
######

Presented here is a DER-encoded x509 RSA certificate. 
Find the modulus of the certificate, giving your answer as a decimal.
"""
from pathlib import Path
from Crypto.PublicKey import RSA

if __name__ == "__main__":
    try:
        der_file: Path = Path(__file__).parent / "2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der"
        with open(der_file, 'rb') as f:
            data = f.read()
            my_key = RSA.import_key(data)
    except FileNotFoundError:
        print("File not found...")
        
    print(f"n: {my_key.n}")