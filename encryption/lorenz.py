# Convert a 4-byte section of the shared secret into an unsigned 32-bit integer
# This function allows us to extract numerical values from different sections of the ECC key.
def get_key_segment(shared_secret, byte_offset): # byte_offset tells Python where to start extracting bytes.
    segment = shared_secret[byte_offset:byte_offset + 4]

    if len(segment) != 4:
        raise ValueError("Invalid shared secret length.")

    return int.from_bytes(segment, byteorder="big") # Converts those four bytes into a single integer. big means big-endian representation, where the most significant byte comes first.


# Generate the Lorenz chaotic sequence
def generate_lorenz_sequence(shared_secret, n_samples):

    if len(shared_secret) != 32:
        raise ValueError("Shared secret must be 32 bytes.")

    if n_samples <= 0:
        raise ValueError("Number of samples must be positive.")

    # Step 1: Derive Lorenz parameters from the shared secret (given)
    sigma = 10 + get_key_segment(shared_secret, 0) / (2 ** 32) 
    rho = 28 + get_key_segment(shared_secret, 4) / (2 ** 32)
    b = 8 / 3

    # Step 2: Derive initial conditions from the shared secret
    # Initial values \(x_0,y_0,z_0\) are derived from the key segments \(K[128:159]\), \(K[160:191]\), and \(K[192:223]\).
    x = get_key_segment(shared_secret, 16) / (2 ** 32)
    y = get_key_segment(shared_secret, 20) / (2 ** 32)
    z = get_key_segment(shared_secret, 24) / (2 ** 32)

    # Step 3: Set the time step
    dt = 0.01

    # Step 4: Discard the first 1000 iterations to remove the transient part of the sequence.
    transient_iterations = 1000

    # Step 5: Generate the sequence
    sequence = []

    total_iterations = transient_iterations + n_samples

    for i in range(total_iterations):

        # Calculate all next values using the previous state
        next_x = x + sigma * (y - x) * dt

        next_y = y + (x * (rho - z) - y) * dt

        next_z = z + (x * y - b * z) * dt

        # Update the current state
        x = next_x
        y = next_y
        z = next_z

        # Store values only after discarding the transient
        if i >= transient_iterations:
            sequence.append(x)

    return sequence
