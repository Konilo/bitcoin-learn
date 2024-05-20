# Integers, bits, bytes, and hexadecimal digits

8 bits = 1 byte = 2 hex (= 0.5 [nibble](https://en.wikipedia.org/wiki/Nibble)). Let’s explain that.

## 1 bit = 1 or 0

2 unique values. So, base 2.

By convention, binary values (a sequence of 1+ bit) are prefixed by `0b` (this convention comes from the C language).

### How to convert binary into integer?

Excerpt from [here](https://www.howtogeek.com/367621/what-is-binary-and-why-do-computers-use-it/):
> “In binary, the first digit is worth 1 in decimal. The second digit is worth 2, the third worth 4, the fourth worth 8, and so on---doubling each time. Adding these all up gives you the number in decimal. So, `1111` (in binary)  $=  8 + 4 + 2 + 1  = 15$ (in decimal)”

### How to convert integer into binary?

Cf. [here](https://www.rapidtables.com/convert/number/decimal-to-binary.html). And a reminder for integer divisions: numerator = (denominator × quotient) + remainder

## 1 byte = a sequence of 8 bits

Base 2 also, as it’s still bits.

[1 byte = 8 bits] has $2^8 = 256$ unique values

A sequence of n bits has $2^n$ unique values. Since two is the number of unique values in a bit, we multiply that n times by itself to find the number of possible bits combinations in the sequence.

## 1 [hexadecimal digit](https://en.wikipedia.org/wiki/Hexadecimal) = `[0-9a-f]` in RegEx

16 unique values, so base 16.

“Hex” is short for “hexadecimal digit(s)/value”. And, by convention, hex values (a sequence of 1+ hex digits) are prefixed by “0x” (this convention comes from the C language). 

A sequence of n hex can have $16^n$ unique values. So, 4 bits ($2^4 = 16$ unique values) convert to 1 hex.

A sequence of 2 hex can have $16^2 = 256$ unique values. Hence, 1 byte ($2^8 = 256$ unique values) can be represented by a sequence of 2 hex.

| hex | `0` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `a`  | `b`  | `c`  | `d`  | `e`  | `f`  |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| int | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |

*Hex-to-int **digit** mapping table used to convert a hex value into an int value*

### How to convert a binary value (a sequence of bits) to a hex value (a sequence of hex digits)?

Cf. “How to Convert Binary to Hex” [here](https://www.binaryhexconverter.com/binary-to-hex-converter). 

### And the converse thing?

Cf. [here](https://www.binaryhexconverter.com/hex-to-binary-converter).

## The interplay between integers, bits and hex

- Humans use integers (`[0-9]` in RegEx, so 10 unique values, so base 10).
- Computers store everything as bits – for technical reasons – which is hard to read for humans
  - Excerpt from [here](https://thecomputersciencebook.com/posts/bits-bytes-and-hexadecimal/): “How long does it take you to tell whether `0b1111111111111111` is the same as `0b111111111111111`?”
- Binary is converted to hex to help humans read it.
  - It would not be ideal to use integers to represent bits because there’s no x such that $2^x = 10$. We can still map `0b1` to integer 1 and `0b0` to integer 0, but then integers 2-9 are unused while we’d want the 10 integer digits to correspond, collectively (1:1 mapping), to all unique values of an n-long sequence of bits.
  - And a value is 4 times more compact in hex than in bits.
    - Following up on the previous example: 
      - Delineate 4-bit sequences: `0b 1111 1111 1111 1111` (spaces are introduced for readability). We have $4*4 = 16$ bits.
      - Each 4-bit sequence can be compacted into a single hex to convert this 16-digit long value into a $16/4 = 4$-digit long value: `0x F F F F` (idem). This is much more human-friendly.
