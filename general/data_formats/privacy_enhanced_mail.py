"""
######
PEM (Privacy Enhanced Mail) is a popular format for sending keys, certificates, 
and other cryptographic material. It looks like:

-----BEGIN RSA PUBLIC KEY-----
MIIBCgKC... (a whole bunch of base64)
-----END RSA PUBLIC KEY-----

It wraps base64-encoded data by a one-line header and footer to indicate how to parse the data within. 
Perhaps unexpectedly, it's important for there to be the correct number of hyphens in the header and footer, 
otherwise cryptographic tools won't be able to recognise the file.
######

Extract the private key d as a decimal integer from the PEM-formatted 
RSA key.
Resources:
-> https://www.cryptologie.net/article/260/asn1-vs-der-vs-pem-vs-x509-vs-pkcs7-vs/
-> https://letsencrypt.org/docs/a-warm-welcome-to-asn1-and-der/
"""
from pathlib import Path
from Crypto.PublicKey import RSA


if __name__ == "__main__":
    try:
        pem_file: Path = Path(__file__).parent / "privacy_enhanced_mail.pem"
        with open(pem_file, 'rb') as f:
            data = f.read()
            my_key = RSA.import_key(data)
    except FileNotFoundError:
        print("File not found...")
    
    print(f"d: {my_key.d}")