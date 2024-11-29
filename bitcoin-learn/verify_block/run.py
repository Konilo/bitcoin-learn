import requests
import hashlib
from operator import rshift, lshift
import logging
import time


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def fetch_last_block_hash() -> str:
    """
    Fetch the latest block data from blockchain.info
    :return: dict - block data
    """
    url = "https://blockchain.info/latestblock?format=json"
    response = requests.get(url)
    last_block_hash = response.json()["hash"]
    return last_block_hash


def get_type_and_size(value):
    if isinstance(value, int):
        # + 7 to complete a potential incomplete byte without adding a new one
        # (1 hex = 8 bits) and // 8 because the remainder can only be caused by
        # the + 7
        return "int", (value.bit_length() + 7) // 8
    elif (
        isinstance(value, str)
        and all(char in "0123456789abcdefABCDEF" for char in value)
        # an hex value must be made of pairs of hex digits
        and len(value) % 2 == 0
    ):
        # 1 byte = 2 hex
        int(1)
        return "hex", len(value) // 2
    else:
        raise ValueError(f"Unsupported type: {type(value)}")


def fetch_block_details(block_hash: str) -> dict:
    """
    Fetch detailed information for a given block by hash
    :param block_hash: str - hash of the block to fetch
    :return: dict - block details
    """

    logger.info("Fetching block details...")
    url = f"https://blockchain.info/rawblock/{block_hash}?format=json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch block details: {response.text}")
    block_details = response.json()

    print(
        "\n#############################\n"
        "### Fetched Block Details ###\n"
        "#############################\n"
        f"{'Field':<15} {'Type':<10} {'Size (bytes)':<15} {'Value'}\n"
        f"{'-'*107}\n"
        f"{'hash':<15} {get_type_and_size(block_details["hash"])[0]:<10} {get_type_and_size(block_details["hash"])[1]:<15} {block_details['hash']}\n"
        f"{'prev_block':<15} {get_type_and_size(block_details['prev_block'])[0]:<10} {get_type_and_size(block_details['prev_block'])[1]:<15} {block_details['prev_block']}\n"
        f"{'time':<15} {get_type_and_size(block_details['time'])[0]:<10} {get_type_and_size(block_details['time'])[1]:<15} {block_details['time']}\n"
        f"{'   (to UTC)':<15} {'':<10} {'':<15} {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(block_details['time']))}\n"
        f"{'ver':<15} {get_type_and_size(block_details['ver'])[0]:<10} {get_type_and_size(block_details['ver'])[1]:<15} {block_details['ver']}\n"
        f"{'mrkl_root':<15} {get_type_and_size(block_details['mrkl_root'])[0]:<10} {get_type_and_size(block_details['mrkl_root'])[1]:<15} {block_details['mrkl_root']}\n"
        f"{'bits':<15} {get_type_and_size(block_details['bits'])[0]:<10} {get_type_and_size(block_details['bits'])[1]:<15} {block_details['bits']}\n"
        f"{'nonce':<15} {get_type_and_size(block_details['nonce'])[0]:<10} {get_type_and_size(block_details['nonce'])[1]:<15} {block_details['nonce']}\n"
    )

    return block_details


def format_binary(value, bit_length, group_size=8):
    """
    Format an integer value as a binary string with groups of bits.

    :param value: The integer to format.
    :param bit_length: Total number of bits to display (default 32).
    :param group_size: Number of bits per group (default 8).
    :return: A formatted binary string (e.g., "00000000 11111111").
    """
    # Convert to binary, remove the "0b" prefix, and pad with leading zeros
    binary_str = f"{value:0{bit_length}b}"

    # Split into groups of group_size bits and join with spaces
    grouped = " ".join(
        binary_str[i : i + group_size]
        for i in range(0, len(binary_str), group_size)
    )
    return grouped


def get_target_from_bits_field(bits: int):
    """
    Obtain the target value (i.e., an integer quantity) from the "bits" field.
    The "bits" field is a 32-bit (4-byte) long binary representation of the
    256-bit long integer target.
    The first byte is the exponent, and the next 3 bytes are the mantissa.
    """

    logger.info("Obtaining the target...")

    logger.info("bits field in binary:")
    logger.info(format_binary(bits, 32))

    # Extract the exponent by shifting the bits to the right by 24 bits (3
    # bytes) thus leaving only the first byte
    # exponent = length (# of bytes) of the target value
    exponent = rshift(bits, 24)
    logger.info("exponent in binary:")
    logger.info(format_binary(exponent, 8))
    logger.info("exponent in decimal:")
    logger.info(exponent)

    # Extract the mantissa by performing a bitwise AND operation with 0xFFFFFF
    # (which is the bitmask for the last 3 bytes, in hexadecimal representation)
    # x & 0xFFFFFF preserves the last 3 bytes of x, and sets the rest of its
    # bytes to 0
    mantissa = bits & 0xFFFFFF
    logger.info("mantissa in binary:")
    logger.info(f"         {format_binary(mantissa, 24)}")

    # `- 3` to remove the 3 bytes of the mantissa from the number of bits the
    # exponent needs to be left-shifted by to get the target
    # `8 *` to convert the exponent from bytes to bits
    # cf. https://developer.bitcoin.org/reference/block_chain.html#target-nbits
    target = lshift(mantissa, 8 * (exponent - 3))
    logger.info("target in binary:")
    logger.info(
        f"{format_binary(mantissa, 24)} (mantissa) followed by {exponent - 3} (exponent - 3) bytes of 0s"
    )

    return target


# Convert hex to bytes, reverse bytes' order, and convert back to hex for proper
# endianess
def reverse_hex(hex_str: str) -> str:
    return bytes.fromhex(hex_str)[::-1].hex()


def int_to_hex_str(int: int) -> str:
    # byteorder is not to reorder the bytes, it's to specify the byte order of
    # the provided int
    return int.to_bytes(4, byteorder="little").hex()


def verify_block_hash(block):
    # Reconstruct the block header
    header_hex = (
        int_to_hex_str(block["ver"])
        + reverse_hex(block["prev_block"])
        + reverse_hex(block["mrkl_root"])
        + int_to_hex_str(block["time"])
        + int_to_hex_str(block["bits"])
        + int_to_hex_str(block["nonce"])
    )

    header_bytes = bytes.fromhex(header_hex)
    reconstructed_hash = (
        hashlib.sha256(hashlib.sha256(header_bytes).digest())
        .digest()[::-1]
        .hex()
    )

    target = get_target_from_bits_field(block["bits"])
    hash_as_int = int(reconstructed_hash, 16)

    print(
        "\n#########################\n"
        "### Hash Verification ###\n"
        "#########################\n"
        f"{'Reconstructed block hash (in base 16/hex):':<53} {reconstructed_hash}\n"
        f"{'Reconstructed block hash == fetched block hash:':<53} {reconstructed_hash == block['hash']}\n"
        f"{'Target (in base 10/decimal):':<53} {target}\n"
        f"{'Reconstructed block hash (in base 10/decimal):':<53} {hash_as_int}\n"
        f"{'Reconstructed block hash < target:':<53} {hash_as_int < target}"
    )

    return {
        "reconstructed_hash": reconstructed_hash,
        "hash_matches": reconstructed_hash == block["hash"],
        "target": target,
        "hash_as_int": hash_as_int,
        "hash_lt_target": hash_as_int < target,
    }


def verify_block(block_hash: str = None) -> None:
    """
    Verify a block's hash by comparing it to the hash reconstructed from the
    block's header fields and checking if it meets the difficulty target.

    :param block_hash: str - hash of the block to verify (if None, the latest)
    """
    if not block_hash:
        logger.info("No block hash provided. Using the latest block hash.")
        block_hash = fetch_last_block_hash()
    block_details = fetch_block_details(block_hash)
    return verify_block_hash(block_details)
