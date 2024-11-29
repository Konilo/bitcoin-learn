import hashlib
import time
import logging


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def pow_iterate(data: str = "Hello world!", difficulty: int = 5) -> tuple:
    """
    Run a simplified proof of work algorithm to find a nonce such that the hash
    of the nonce appended to the data starts with 'difficulty' number of zero
    bits.

    :param data: str - data to be hashed
    :param difficulty: int - number of zero bits the hash must start with
    :return: tuple - returns the nonce and the hash
    """
    logger.info(
        f'Starting proof of work iteration on "{data}" with difficulty {difficulty}...'
    )

    nonce = 0
    start_time = time.time()
    while True:
        # Append the nonce to the original data and encode it to bytes via UTF-8
        input_data = f"{data}{nonce}".encode("utf-8")

        hash_hex = hashlib.sha256(input_data).hexdigest()

        # [2:] removes the '0b' prefix from the binary representation
        # zfill(256) ensures the binary representation is 256 bits long
        hash_binary = bin(int(hash_hex, 16))[2:].zfill(256)

        # The difficulty is a threshold: starting with <difficulty> 0s means that
        # the hash (in decimal) is lower than 2 ** (256 - difficulty)
        if hash_binary.startswith("0" * difficulty):
            end_time = time.time()
            print(
                "###############\n"
                "### Results ###\n"
                "###############\n"
                f"{'First valid nonce found:':<26}{nonce}\n"
                f"{'Hash:':<26}{hash_hex}\n"
                f"{'Time taken:':<26}{round(end_time - start_time, 3)} seconds"
            )
            return nonce, hash_hex
        nonce += 1
