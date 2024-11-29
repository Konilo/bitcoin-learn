# Bitcoin Learn

Bitcoin is a software that allows individuals to own and exchange bitcoins without the intervention of a third party.
To achieve this, Bitcoin drew from many mathematical and computer science concepts.
In this repository, I propose an exploration of some of those fundamental tools.

**Finance or trading are deliberately put out of scope. Bitcoin Learn is in no way meant to promote bitcoin as an investment.**
Rather, I use Bitcoin as a pretext to manipulate and understand new concepts.

Each topic I cover corresponds to a subdirectory in `bitcoin-learn/`:
- `convert_number`: positional numeral systems (binary, decimal, hexadecimal)
- `pow_iterate`: fundamentals of proof of work
- `verify_block`: hashing and consensus verification on actual Bitcoin blocks
- `compute_reorg_attack_probability`: probabilities and the risk mining power concentration poses

## Getting Started

To get started with the repository, clone it to your local machine:

```sh
git clone https://github.com/yourusername/bitcoin-learn.git
cd bitcoin-learn
make run-dev-env
```