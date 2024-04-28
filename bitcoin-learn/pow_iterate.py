import hashlib
import time


def find_nonce(data, difficulty=4):
    """
    This function finds a valid nonce for the given data such that the hash of the nonce appended
    to the data starts with 'difficulty' number of zero bits.

    :param data: str - data to be hashed
    :param difficulty: int - number of zero bits the hash must start with
    :return: tuple - returns the nonce and the hash
    """
    prefix = "0" * difficulty
    nonce = 0
    start_time = time.time()

    while True:
        # Append the nonce to the original data
        input_data = f"{data}{nonce}".encode()
        # Calculate the SHA-256 hash of the input data
        hash_result = hashlib.sha256(input_data).hexdigest()
        # Check if the hash meets the difficulty criteria
        if hash_result.startswith(prefix):
            print(f"Nonce found: {nonce}")
            print(f"Hash: {hash_result}")
            print(f"Time taken: {time.time() - start_time} seconds")
            return nonce, hash_result
        nonce += 1


# Example use case
data = "Hello, this is a test block"
difficulty = 5
find_nonce(data, difficulty)
