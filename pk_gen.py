from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
import datetime

# Path to your PKCS8 private key
private_key_path = 'cloudfront_private_key.pem'

# Function to load the private key
def rsa_signer(message):
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    # No need to encode the message since it is already in bytes format
    return private_key.sign(
        message,  # Directly use the message as it's in bytes
        padding.PKCS1v15(),
        hashes.SHA1()
    )

# CloudFront Key Pair ID
key_id = 'K1K4ZBNPQBSVLW'

# CloudFront signer using the private key
cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

# URL to be signed
url = 'https://d1rl0r14vd2l8a.cloudfront.net'

# Set the expiration time for the signed URL (e.g., 1 hour from now)
expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=100)

# Generate the signed URL
signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expires_at)
print(f"Signed URL: {signed_url}")