# Extract a 32-bit integer from four bytes of the shared secret
def get_key_segment(shared_secret, byte_offset):

    segment = shared_secret[byte_offset:byte_offset + 4]

    if len(segment) != 4:
        raise ValueError("Invalid shared secret length.")

    return int.from_bytes(segment, byteorder="big")


# Generate the Rössler chaotic sequence
def generate_rossler_sequence(shared_secret, n_samples):

    # Validate inputs
    if len(shared_secret) != 32:
        raise ValueError("Shared secret must be 32 bytes.")

    if n_samples <= 0:
        raise ValueError("Number of samples must be positive.")

    # Step 1: Derive Rössler parameters from the shared secret
    a = 0.2 + get_key_segment(shared_secret, 8) / (2 ** 32)

    c = 5.7 + get_key_segment(shared_secret, 12) / (2 ** 32)

    b = 0.2

    # Step 2: Derive initial conditions from the shared secret
    x = get_key_segment(shared_secret, 16) / (2 ** 32)

    y = get_key_segment(shared_secret, 20) / (2 ** 32)

    z = get_key_segment(shared_secret, 24) / (2 ** 32)

    # Step 3: Set the time step
    dt = 0.01

    # Step 4: Discard the first 1000 iterations
    transient_iterations = 1000

    # Step 5: Generate the sequence
    sequence = []

    total_iterations = transient_iterations + n_samples

    for i in range(total_iterations):

        # Calculate the next values using the current state
        next_x = x + (-y - z) * dt

        next_y = y + (x + a * y) * dt

        next_z = z + (b + z * (x - c)) * dt

        # Update the current state
        x = next_x
        y = next_y
        z = next_z

        # Store values only after discarding the transient
        if i >= transient_iterations:
            sequence.append(x)

    return sequence
