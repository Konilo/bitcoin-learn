import os
import sys

# Allow imports from the parent directory
dir_abspath = os.path.dirname(__file__)
parent_dir_abspath = os.path.dirname(dir_abspath)
sys.path.append(parent_dir_abspath)

from verify_block.run import verify_block
from pow_iterate.run import pow_iterate
from convert_number.run import convert_number
from compute_reorg_attack_probability.run import (
    compute_reorg_attack_probability,
)


def test_verify_block():
    block_hash = (
        "000000000000000000006ac894c3d62bd4c37ba926e0580e5c99ca4466aee835"
    )
    verification_results = verify_block(block_hash)
    assert verification_results["reconstructed_hash"] == block_hash
    assert verification_results["hash_matches"] == True
    assert (
        verification_results["target"]
        == 263561359269705708657179707992723614632672251070119936
    )
    assert (
        verification_results["hash_as_int"]
        == 39952458056013901956252452617013828782555569887045685
    )
    assert verification_results["hash_lt_target"] == True


def test_pow_iterate():
    assert pow_iterate("Hello world!", 5) == (
        23,
        "03e5fd995bf222866e9e71bf7e9c455f5a8f6590e6ffebc7036f57ca507c6eb7",
    )


def test_convert_number():
    assert convert_number(1101101100101, 2, 16) == "1B65"
    assert convert_number("A12F8", 16, 2) == "10100001001011111000"
    assert convert_number(1010101110, 2, 10) == "686"
    assert convert_number(6348, 10, 2) == "1100011001100"
    assert convert_number(36456, 10, 16) == "8E68"
    assert convert_number("AF78", 16, 10) == "44920"

    assert (
        convert_number(0, 2, 16)
        == convert_number("0", 16, 2)
        == convert_number(0, 2, 10)
        == convert_number(0, 10, 2)
        == convert_number(0, 10, 16)
        == convert_number("0", 16, 10)
        == "0"
    )


def test_compute_reorg_attack_probability():
    assert (
        compute_reorg_attack_probability(0.1, 4, "original")
        == 0.0034552434664851736
    )
    assert (
        compute_reorg_attack_probability(0.1, 4, "modified")
        == 0.00047279024929107894
    )
