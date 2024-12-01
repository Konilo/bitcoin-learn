import logging
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.exceptions import InvalidSignature
import hashlib


def setup_logger(name, log_format):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


logger = setup_logger(
    "NARRATIVE",
    "NARRATIVE %(message)s",
)


class Wallet:
    def __init__(self):
        self.logger = setup_logger(
            f"Wallet-{id(self)}",
            "WALLET %(message)s",
        )
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()
        self.logger.info("Wallet, private key, and public key created.")

    def make_tx(self, utxo_to_spend: dict, recipient_pub_key):
        formatted_recipient_pub_key = self.format_pub_key(recipient_pub_key)
        tx_data = (str(utxo_to_spend) + formatted_recipient_pub_key).encode(
            "utf-8"
        )
        hash_for_signature = hashlib.sha256(tx_data).hexdigest().encode("utf-8")
        sender_signature = self.private_key.sign(
            hash_for_signature,
            ec.ECDSA(hashes.SHA256()),
        )
        return {
            "recipient_pub_key": formatted_recipient_pub_key,
            "hash_for_signature": hash_for_signature,
            "sender_signature": sender_signature,
        }

    @staticmethod
    def format_pub_key(public_key):
        return str(
            public_key.public_bytes(
                Encoding.DER,
                PublicFormat.SubjectPublicKeyInfo,
            )
        )


class Node:
    def __init__(self):
        self.logger = setup_logger(
            f"Wallet-{id(self)}",
            "NODE %(message)s",
        )

    def verify_tx(self, tx: dict, sender_pub_key):
        try:
            sender_pub_key.verify(
                tx["sender_signature"],
                tx["hash_for_signature"],
                ec.ECDSA(hashes.SHA256()),
            )
        except InvalidSignature:
            self.logger.warning(
                "Transaction rejected because the signature is invalid."
            )
        except Exception as e:
            self.logger.error(f"An unknown error occurred: {e}")
            raise
        else:
            self.logger.info("Transaction verified.")


def transact():
    """
    Simulate a simplified transaction using asymmetric cryptography.
    """

    # The Bitcoin network is represented by a single node for simplicity
    node = Node()

    logger.info("Persons A, B, and C each create their wallet")
    wallet_a = Wallet()
    wallet_b = Wallet()
    wallet_c = Wallet()

    # We'll consider that wallet A receives an initial transaction e.g., from the
    # Bitcoin network itself because they mined a block.
    # (For simplicity, I don't consider transactions amounts. We'll consider that
    # transactions each cover one bitcoin.)
    initial_tx = {
        "recipient_pub_key": wallet_a.public_key,
        "hash_for_signature": hashlib.sha256(
            str(
                "No input tx" + Wallet.format_pub_key(wallet_a.public_key)
            ).encode("utf-8")
        )
        .hexdigest()
        .encode("utf-8"),
        "sender_signature": None,
    }

    logger.info(
        "Persons A & B make business: A needs to pay B, after what B will deliver"
        + " a good or service to A."
    )
    logger.info(
        "B provides their public key (which, essentially, is what a real Bitcoin"
        + " wallet address is) to A."
    )
    wallet_b_pub_key = wallet_b.public_key

    logger.info(
        "But person C obtains A's public key to try to steal their bitcoin."
    )
    logger.info(
        "To do that they must make a transaction from A to themself and falsify A's"
        + " signature which requires A's private key."
    )
    logger.info(
        "But C cannot guess A's private key, even using A's public key."
        + " That's the power of asymmetric cryptography."
    )
    logger.info(
        " So, C resorts to signing the malicious transaction with their own"
        + " private key."
    )
    wallet_a_pub_key = wallet_a.public_key
    malicious_tx = wallet_c.make_tx(
        initial_tx,
        wallet_c.public_key,
    )

    logger.info(
        "The Bitcoin network rejects the transaction because, knowing A's"
        + " public key, it detects that the transaction intends to spend"
        + " bitcoin owned by A but is not signed by A."
    )
    logger.info(
        "Asymmetric cryptography allows the network to verify the transaction"
        + " without revealing the private key."
    )
    node.verify_tx(
        malicious_tx,
        wallet_a_pub_key,
    )

    logger.info(
        "Finally, A makes the legitimate transaction to B, signing it with"
        + " their private key."
    )
    legit_tx = wallet_a.make_tx(
        initial_tx,
        wallet_b_pub_key,
    )
    node.verify_tx(
        legit_tx,
        wallet_a_pub_key,
    )
