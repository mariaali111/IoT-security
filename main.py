from encryption.ecc import (
    generate_key_pair,
    derive_shared_secret,
    export_public_key,
    import_public_key
)
from encryption.lorenz import generate_lorenz_sequence
from encryption.rossler import generate_rossler_sequence
from encryption.lre import encrypt, decrypt


def main():

    print("===== ECC KEY EXCHANGE =====")

    # Device A generates its keys
    private_A, public_A = generate_key_pair()

    # Device B generates its keys
    private_B, public_B = generate_key_pair()

    print("\nDevice A keys generated.")
    print("Device B keys generated.")

    # Simulate public key transmission
    transmitted_A = export_public_key(public_A)
    transmitted_B = export_public_key(public_B)

    received_A = import_public_key(transmitted_A)
    received_B = import_public_key(transmitted_B)

    print("\nPublic keys exchanged successfully.")

    # Both devices calculate their shared secret
    shared_A = derive_shared_secret(
        private_A,
        received_B
    )

    shared_B = derive_shared_secret(
        private_B,
        received_A
    )

    print("\nDevice A Shared Secret:", shared_A.hex())
    print("Device B Shared Secret:", shared_B.hex())

    # Verify that both secrets match
    if shared_A == shared_B:
        print("\nSUCCESS: Both devices generated the same shared secret.")
    else:
        print("\nERROR: Shared secrets do not match.")

    print("\nShared Secret Length:", len(shared_A), "bytes")


    print("\n===== LORENZ CHAOTIC SYSTEM =====")

    lorenz_sequence = generate_lorenz_sequence(shared_A, 10)

    print("Generated Lorenz sequence:")
    for i, value in enumerate(lorenz_sequence):
        print(f"x[{i}] = {value}")

    print("\nSequence length:", len(lorenz_sequence))

    print("\n===== ROSSLER CHAOTIC SYSTEM =====")

    rossler_sequence = generate_rossler_sequence(shared_A, 10)

    print("Generated Rössler sequence:")

    for i, value in enumerate(rossler_sequence):
        print(f"x[{i}] = {value}")

    print("\nSequence length:", len(rossler_sequence))

    print("\n===== LRE ENCRYPTION AND DECRYPTION =====")

    # Original message
    message = b"Hello IoT Security"

    print("\nOriginal Message:", message.decode())

    # Encrypt the message
    ciphertext = encrypt(message, shared_A)

    print("\nCiphertext (hex):", ciphertext.hex())

    # Decrypt the ciphertext
    decrypted_message = decrypt(ciphertext, shared_B)

    print("\nDecrypted Message:", decrypted_message.decode())

    # Verify the result
    if message == decrypted_message:
        print("\nSUCCESS: LRE encryption and decryption verified.")
    else:
        print("\nERROR: Decrypted message does not match.")


if __name__ == "__main__":
    main()
