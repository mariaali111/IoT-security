from encryption.lorenz import generate_lorenz_sequence
from encryption.rossler import generate_rossler_sequence


# Generate the combined keystream
def generate_keystream(shared_secret, n_samples):

    # Generate Lorenz sequence
    lorenz_sequence = generate_lorenz_sequence(
        shared_secret,
        n_samples
    )

    # Generate Rössler sequence
    rossler_sequence = generate_rossler_sequence(
        shared_secret,
        n_samples
    )

    # Combine both sequences using XOR
    combined_sequence = []

    for i in range(n_samples):

        lorenz_value = int(lorenz_sequence[i] * 10**6)

        rossler_value = int(rossler_sequence[i] * 10**6)

        combined_value = lorenz_value ^ rossler_value

        combined_sequence.append(combined_value)

    return combined_sequence


# Encrypt plaintext using the LRE keystream
def encrypt(plaintext, shared_secret):

    if not isinstance(plaintext, bytes):
        raise TypeError("Plaintext must be in bytes.")

    if len(plaintext) == 0:
        raise ValueError("Plaintext cannot be empty.")

    # One keystream value is required for each plaintext byte
    keystream = generate_keystream(
        shared_secret,
        len(plaintext)
    )

    ciphertext = bytearray()

    for i in range(len(plaintext)):

        key_byte = keystream[i] % 256

        encrypted_byte = plaintext[i] ^ key_byte

        ciphertext.append(encrypted_byte)

    return bytes(ciphertext)


# Decrypt ciphertext using the LRE keystream
def decrypt(ciphertext, shared_secret):

    if not isinstance(ciphertext, bytes):
        raise TypeError("Ciphertext must be in bytes.")

    if len(ciphertext) == 0:
        raise ValueError("Ciphertext cannot be empty.")

    # Regenerate the same keystream
    keystream = generate_keystream(
        shared_secret,
        len(ciphertext)
    )

    plaintext = bytearray()

    for i in range(len(ciphertext)):

        key_byte = keystream[i] % 256

        decrypted_byte = ciphertext[i] ^ key_byte

        plaintext.append(decrypted_byte)

    return bytes(plaintext)
