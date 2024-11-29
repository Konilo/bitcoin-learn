# Bitcoin Learn

Bitcoin is a software that allows individuals to own and exchange bitcoins without the intervention of a third party.
To achieve this, Bitcoin drew from many mathematical and computer science concepts.
In this repository, I propose an exploration of some of those fundamental tools.

**Finance or trading are deliberately put out of scope. Bitcoin Learn is in no way meant to promote bitcoin as an investment.**
Rather, I use Bitcoin as a pretext to manipulate and understand new concepts.

Each topic I cover corresponds to a subdirectory in `bitcoin-learn/`:
- [`convert_number`](https://github.com/Konilo/bitcoin-learn/blob/main/bitcoin-learn/convert_number/notes.md): positional numeral systems (binary, decimal, hexadecimal)
- [`pow_iterate`](https://github.com/Konilo/bitcoin-learn/blob/main/bitcoin-learn/pow_iterate/run.py): fundamentals of proof of work
- [`verify_block`](https://github.com/Konilo/bitcoin-learn/blob/main/bitcoin-learn/verify_block/run.py): hashing and consensus verification on actual Bitcoin blocks
- [`compute_reorg_attack_probability`](https://github.com/Konilo/bitcoin-learn/blob/main/bitcoin-learn/compute_reorg_attack_probability/notes.md): probabilities and the risk mining power concentration poses

## Getting Started

To get started with the repository, clone it to your local machine:

```sh
git clone git@github.com:yourusername/bitcoin-learn.git
cd bitcoin-learn
make run-dev-env
```