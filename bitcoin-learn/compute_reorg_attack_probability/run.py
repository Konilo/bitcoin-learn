import math
import logging


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def compute_reorg_attack_probability(q: float, z: int, formula: str):
    """
    Compute the probability of success of a reorg double spending attack.

    :param q: float - share of the network's hashrate possessed by the attacker
    :param z: int - number of blocks mined on the legitimate chain from (i) the
                    moment the block containing the transaction was mined
                    (included) to (ii) the moment the merchant delivers what the
                    attacker paid for
    :param formula: str - formula to use to compute the probability of success
                         of the reorg attack.
    """

    if q < 0 or q > 1:
        raise ValueError("q must be in [0, 1]")
    if z < 0:
        raise ValueError("z must be positive")

    # share of the network's hashrate possessed by the honest nodes
    p = 1 - q

    # expected number of blocks mined by the attacker during the period
    # described above in z
    lambda_blocks = z * (q / p)

    prob = 1

    # + 1 because we want to iterate from 0 to z (both bounds included)
    for k in range(z + 1):

        # 'poisson' is the probability that the attacker mined k blocks
        poisson = math.exp(-lambda_blocks)
        for i in range(1, k + 1):
            poisson *= lambda_blocks / i

        # 'not_catch_up_prob' is the probability
        if formula == "original":
            attack_failure_probability = 1 - (q / p) ** (z - k)
        elif formula == "modified":
            # The "+ 1" below is not present in Satoshi's formula but I propose
            # to add it to meausre the probability the attacker's chain
            # surpasses the honest one, and doesn't just catch up to it
            # which is not enough for a successful attack (cf. the README).
            attack_failure_probability = 1 - (q / p) ** (z - k + 1)
        else:
            raise ValueError("Formula argument is invalid")

        # For eack k, remove from 1 the probability that k blocks were mined by
        # the attacker (poisson) * the probability that the attack fails given
        # k. At the end, what remains is the probability of success.
        prob -= poisson * attack_failure_probability

    logger.info(f"Regorg attack probability = {prob * 100:.2f}%")
    return prob
