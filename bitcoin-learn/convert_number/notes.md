# Binary, decimal, and hexadecimal numeral systems

A single integer value can be represented in many ways. Each way is formally called a [*numeral system*](https://en.wikipedia.org/wiki/Numeral_system) (NS) and each NS gives rise to its own *number* representing the *value*.
- Humans commonly use the decimal NS which uses 10 digits (0-9).
- Computers store and manipulate information using the binary NS which relies on 2 digits (0 and 1).
- And, to bridge the gap between the two (we'll see further down how actually this bridges the gap), one can use the hexadecimal NS which uses 16 digits (0-9 and A-F).

Bitcoin, as a software, directly manipulates binary and hexadecimal numbers. Several notions are key to understand the main operations that make its blockchain work: block hashes are integer values that are usually represented in hexadecimal, the size of the information fields comprised in a block is expressed in bytes, etc.

To cover the basics, let's explain why 8 bits = 1 byte = 2 hex and cover conversion between the 3 NSs.


## Binary numeral system

In the binary NS, only 2 digits exist (0 and 1). The binary NS being a positional NS, having 2 digits means that it's a [base-2](https://en.wikipedia.org/wiki/Radix) NS.


### 1 bit = [0-1]

The bit (short for binary digit) is the minimal unit of information in computers.

By convention, a binary number (a sequence of 1+ bit) is prefixed by `0b` (this convention comes from the C language).


#### How to convert binary into decimal?

The process is simple:
> “In binary, the first digit is worth 1 in decimal. The second digit is worth 2, the third worth 4, the fourth worth 8, and so on---doubling each time. Adding these all up gives you the number in decimal. So, `1111` (in binary)  $=  8 + 4 + 2 + 1  = 15$ (in decimal)”
 
 *Excerpt from [here](https://www.howtogeek.com/367621/what-is-binary-and-why-do-computers-use-it/).*


### How to convert decimal into binary?

THe other way round, it gets a bit more complex, cf. [here](https://www.rapidtables.com/convert/number/decimal-to-binary.html). 

(NB: quick reminder for a integer divisions: $numerator = (denominator × quotient) + remainder$.)


### 1 byte = a sequence of 8 bits

When we talk about bytes, we are still using the binary NS since a byte is a sequence of 8 binary digits.

Since 2 is the number of unique possible values in a bit, we multiply that n times by itself to find the number of possible bits combinations in the sequence:
- a sequence of n bits has $2^n$ unique values,
- [1 byte = 8 bits] can have $2^8 = 256$ unique values.


## Hexadecimal numeral system

In the hexadecimal NS, there are 16 digits (0-9 and A-F). This NS being a positional one (as binary and decimal), having 16 digits means that it's a base-16 NS.


### 1 hexadecimal digit = `[0-9A-F]`

“hex” is short for hexadecimal. By convention, hex numbers (a sequence of 1+ hex digits) are prefixed by `0x` (this convention comes from the C language). 

A sequence of n hex digits can have $16^n$ unique values. So, 4 bits ($2^4 = 16$ unique values) convert to 1 hex.

A sequence of 2 hex can have $16^2 = 256$ unique values. Hence, 1 byte ($2^8 = 256$ unique values) can be represented by a sequence of 2 hex.

| hex | `0` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `a`  | `b`  | `c`  | `d`  | `e`  | `f`  |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| decimal | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |

*Hex-to-decimal digit mapping table used to convert a hex value into a decimal value*


#### How to convert binary into hexadecimal?

Cf. “How to Convert Binary to Hex” [here](https://www.binaryhexconverter.com/binary-to-hex-converter). 


#### How to convert hexadecimal to binary?

Cf. [here](https://www.binaryhexconverter.com/hex-to-binary-converter).


## The interplay between the binary and hexadecimal numeral systems

- Computers store everything as bits – for technical reasons – which is hard to read for humans
  - Excerpt from [here](https://thecomputersciencebook.com/posts/bits-bytes-and-hexadecimal/): “How long does it take you to tell whether `0b1111111111111111` is the same as `0b111111111111111`?”
- Binary is converted to hexadecimal to help humans read it.
  - It would not be ideal to use decimal digits to represent bits because there’s no x such that $2^x = 10$. We can still map binary `0b1` to decimal 1 and binary `0b0` to decimal 0, but then decimal digits 2-9 are unused while we’d want the 10 integer digits to correspond, collectively (1:1 mapping), to all unique values of an n-long sequence of bits.
  - And a value is 4 times more compact represetned in hexadecimal than in binary.
    - Following up on the previous example: 
      - Delineate 4-bit sequences: `0b 1111 1111 1111 1111`. We have $4*4 = 16$ bits. (NB: a 4 sequence of 4 bits is a [nibble](https://en.wikipedia.org/wiki/Nibble).)
      - Each 4-bit sequence can be compacted into a single hexadecimal digit to convert this 16-digit long value into a $16/4 = 4$-digit long value: `0x F F F F`. This is much more human-friendly.
