import hashlib
import time

(hexdigest := hashlib.sha256("input_data".encode()).hexdigest())
# length
len(hexdigest)


ver = 536977408
bytes_representation = ver.to_bytes(4, byteorder="little")
print(" ".join(f"{byte:02x}" for byte in bytes_representation))
bytes_representation.hex()

hex_str = "0000000000000000000296d96aaa1330d0f1511ca0cd07598664566380f52ff1"
print(" ".join(f"{byte:02x}" for byte in bytes.fromhex(hex_str)))
print(" ".join(f"{byte:02x}" for byte in bytes.fromhex(hex_str)[::-1]))
bytes.fromhex(hex_str)[::-1].hex()


def bits_to_target(bits: int) -> int:
    # Calculate the target value from the bits field
    exponent = bits >> 24
    mantissa = bits & 0xFFFFFF
    target = mantissa * 2 ** (8 * (exponent - 3))
    return target


from operator import rshift


bits = 38
shifted_bits = rshift(bits, 2)
print(bin(bits))
print(bin(shifted_bits))

175509739761080105932380337066075551144639533224473548 < 305996059309608474887223697110640892108382252455428096
