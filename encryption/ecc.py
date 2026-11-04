from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


# Step 1: Generate ECC private and public keys
def generate_key_pair():

    # Generate a random private key using Brainpool P256r1
    private_key = ec.generate_private_key(ec.BrainpoolP256R1())

    # Generate the corresponding public key (The public key is mathematically derived from the private key)
    public_key = private_key.public_key()

    return private_key, public_key


# Step 2: Derive the shared secret
def derive_shared_secret(private_key, peer_public_key):  # The function takes two arguments: The device's own private key, The other device's public key.

    # Perform Elliptic Curve Diffie-Hellman
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)

    return shared_secret


# These functions will become useful when we simulate communication between devices.
# Step 3: Export public key into bytes
def export_public_key(public_key):

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    return public_bytes


# Step 4: Import public key from bytes
def import_public_key(public_bytes):

    public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.BrainpoolP256R1(),
        public_bytes
    )

    return public_key

# A public key is converted into bytes before transmission and reconstructed at the receiving end.