import math


def reorg_attack_probability(q: float, z: int):
    # Probability of success of a reorg double spending attack
    # q: share of the network's hashrate possessed by the attacker
    # z: number of blocks mined on the legitimate chain from (i) the moment the block containing the transaction was mined (included) to (ii) the moment the merchant delivers what the attacker paid for

    # share of the network's hashrate possessed by the honest nodes
    p = 1 - q

    # expected number of blocks mined by the attacker during the period described above in z
    lambda_blocks = z * (q / p)

    prob = 1

    # + 1 because we want to iterate from 0 to z (both bounds included) while range(z) spans over 0 to z - 1
    for k in range(z + 1):
        poisson = math.exp(-lambda_blocks)
        for i in range(1, k):
            poisson *= lambda_blocks / i
        prob -= poisson * (1 - (q / p) ** (z - k))  # TODO add + 1

    return prob


reorg_attack_probability(0.1, 4)


def attacker_success_probability(q, z):
    # Calculate the probability of a successful reorganization attack by an attacker
    # q: Share of the network's hashrate possessed by the attacker
    # z: Number of blocks the honest chain has mined since the fork

    p = 1.0 - q  # share of the network's hashrate possessed by the honest nodes
    lambda_blocks = z * (q / p)  # expected number of blocks mined by the attacker

    sum_prob = 1.0  # Initialize the sum of probabilities where the attacker fails
    for k in range(z + 1):
        # Calculate the Poisson probability of the attacker mining exactly k blocks
        poisson = math.exp(-lambda_blocks)  # Probability of k=0
        for i in range(1, k + 1):
            poisson *= lambda_blocks / i  # Multiply by lambda/i for each count up to k

        # Calculate the probability of not catching up from this point
        not_catch_up_prob = 1 - (q / p) ** (z - k)
        sum_prob -= poisson * not_catch_up_prob

    return sum_prob


attacker_success_probability(0.1, 4)
