import requests
import hashlib
import json
from operator import rshift, lshift


BLOCK_HEADER_FIELDS = ["ver", "prev_block", "mrkl_root", "time", "bits", "nonce"]

def fetch_last_block():
    # Fetch the latest block data from blockchain.info
    url = "https://blockchain.info/latestblock?format=json"
    response = requests.get(url)
    block = response.json()
    return block


def fetch_block_details(block_hash):
    # Fetch detailed information for a given block by hash
    url = f"https://blockchain.info/rawblock/{block_hash}?format=json"
    response = requests.get(url)
    block_details = response.json()

    print("\n### Block Details ###")
    print(f"hash ({type(block_details["hash"])}):{block_details["hash"]}")
    print(f"prev_block ({type(block_details["prev_block"])}): {block_details["prev_block"]}")
    print(f"time ({type(block_details["time"])}): {block_details["time"]}")
    print(f"ver ({type(block_details["ver"])}): {block_details["ver"]}")
    print(f"mrkl_root ({type(block_details["mrkl_root"])}): {block_details["mrkl_root"]}")
    print(f"bits ({type(block_details["bits"])}): {block_details["bits"]}")
    print(f"nonce ({type(block_details["nonce"])}): {block_details["nonce"]}")

    return block_details


def bits_to_target(bits):
    # Calculate the target value from the bits field
    # The bits field is a 32-bit (4 bytes) long representation of the 256-bit long integer target
    # The first byte is the exponent, and the next 3 bytes are the mantissa

    # Extract the exponent by shifting the bits to the right by 24 bits (3 bytes) thus leaving only the first byte
    # exponent = length of the target value, in bytes
    exponent = rshift(bits, 24)

    # Extract the mantissa by performing a bitwise AND operation with 0xFFFFFF (which is the bitmask for the last 3 bytes, in hexadecimal representation)
    # x & 0xFFFFFF preserves the last 3 bytes of x, and sets the rest of its bytes to 0
    mantissa = bits & 0xFFFFFF

    # https://developer.bitcoin.org/reference/block_chain.html#target-nbits
    # `- 3` to remove the 3 bytes of the mantissa represents from the number of bits the exponent needs to be left-shifted by to get the target
    # `8 *` to convert the exponent from bytes to bits
    target = lshift(mantissa, 8 * (exponent - 3))
    return target


# Convert hex to bytes, reverse bytes' order, and convert back to hex for proper endianess
def reverse_hex(hex_str: str) -> str:
    return bytes.fromhex(hex_str)[::-1].hex()


def int_to_hex_str(int: int) -> str:
    # byteorder is not to reorder the bytes, it's to specify the byte order of the provided int
    return int.to_bytes(4, byteorder="little").hex()


def verify_block(block):
    # Reconstruct the block header
    header_hex = (
        int_to_hex_str(block["ver"])
        + reverse_hex(block["prev_block"])
        + reverse_hex(block["mrkl_root"])
        + int_to_hex_str(block["time"])
        + int_to_hex_str(block["bits"])
        + int_to_hex_str(block["nonce"])
    )

    header_bin = bytes.fromhex(header_hex)
    reconstructed_hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()[::-1].hex()

    target = bits_to_target(block["bits"])
    hash_int = int(reconstructed_hash, 16)

    print("\n### Verification ###")
    print("Calculated Hash:", reconstructed_hash)
    print("Reconstructed block hash == fetched block hash:", block["hash"] == reconstructed_hash)
    print("Target (as int, converted from bits):", target)
    print("Reconstructed Block Hash as int:", hash_int)
    print("Hash < target:", hash_int < target)


def run():
    last_block = fetch_last_block()
    block_hash = last_block["hash"]
    block_details = fetch_block_details(block_hash)
    verify_block(block_details)

run()
