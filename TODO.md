# Ideas & TODO

- General & misc
  - Migrate "Bitcoin tech" GDoc here. And make a pedagogical md for each subscript. Its scope would be what I wanted/needed to synthesize/rephrase/detail myself to learn/understand, by opposition to what didn't required it which I can just include links to.
  - Move block fetching utils in `utils/`.
  - Implement `main.py`; each subscript in its own subdir with it's CLI parsing and config.
  - README with a quick desc. for each subscript and an automatically (dynamically) created link to its CLI.
  - Make a commented, md copy of the white paper. Use it as the red thread of the repo. How to learn Bitcoin with repo?
    - Read the README.md (e.g., on GitHub) to get a sense of the repo aims to do. The README.md, at the end, directs to the commented white paper
    - Read the commented white paper. Key terms or paragraphs are be explained, via a comment, using simple text, links to ressources (cf. 1st point in General & misc), and/or a subscript created in the repo. In the case of a subscript, the comment directs to the md of the subscript which provides pedagogical info/links about the concept, shows how to run the subscript corresponding the concept in question, and directs to the actual code to understand the underlying technology in details.

- `verify_block`
  - Allow the verification of the last block or of block header elements provided via the CLI.
  - Finish implementation of `BLOCK_HEADER_FIELDS`.

- `pow_iterate`
  - Fetch `bits` from a block given via the CLI and reproduce its PoW.
  - Make the PoW more accurate (correct what's hashed, use double SHA-256, etc. cf. `verify_block`; btw, there may be some common func to move to utils).
  - Implement a mode where we reproduce the PoWs from oldest to newest blocks (with a timeout when it gets too long).
  - Is it validate instead of verify?

- `track_address_tx`
  - Via the args, make it possible to track Satoshi's tx.
  - If not too heavy, make it possible to reconstruct the balance of an address over time.
  - Make tests.
  - Something about UTXOs?
  - Is ir "address" or "public key"?

- Something about fees?

- Something about mining centralization? E.g., evolution of the nb of unique addresses that received a block subsidy per month. But that's maybe a bad proxy.

- Something to monitor the mempool?