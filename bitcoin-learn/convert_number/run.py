import logging


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Supported digits (keys) and their values in decimal (values)
SUPPORTED_DIGITS = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
}

SUPPORTED_SYSTEMS = {
    "binary": 2,
    "decimal": 10,
    "hexadecimal": 16,
}

STOP_SYMBOL = "^"


class Number:
    """
    Number in a positional numeral system and converter to other positional
    numeral systems
    """

    def __init__(self, number: int | str, base: int) -> None:
        """
        Initialize the number and its base

        :param number: int | str - little endian number in the provided base
        :param base: int - base of the provided number
        """

        self.provided_number = str(number)
        self.provided_base = base

        if self.provided_base not in SUPPORTED_SYSTEMS.values():
            raise ValueError("Unsupported base was provided")

        self.digits_in_provided_system = list(SUPPORTED_DIGITS.keys())[
            : self.provided_base
        ]

        if not all(
            digit in self.digits_in_provided_system
            for digit in self.provided_number
        ):
            raise ValueError(
                "Invalid digits are present in the number provided"
            )

        # number_in_decimal is the center point from which all conversions are
        # made
        if self.provided_base == 10:
            self.number_in_decimal = int(self.provided_number)
        else:
            self.number_in_decimal = self._convert_provided_number_to_decimal()

    def _convert_provided_number_to_decimal(self):
        decimal_number = 0
        # Switch to big endian for practicality
        for idx, digit in enumerate(reversed(self.provided_number)):
            decimal_number += SUPPORTED_DIGITS[digit] * self.provided_base**idx
        return decimal_number

    def to_base(self, target_base):
        # Check
        if target_base not in SUPPORTED_SYSTEMS.values():
            raise ValueError("Unsupported base was provided")

        if target_base == self.provided_base:
            number_to_base = self.provided_number
        if target_base == 10:
            number_to_base = str(self.number_in_decimal)
        else:
            # Conversion to a base that's not the provided one nor base-10
            # Add 1 until the equivalent number in the target base is reached
            number_to_base_as_list = ["0"]  # initiation
            for _ in range(self.number_in_decimal):
                number_to_base_as_list = self._increment_by_one(
                    number_to_base_as_list, target_base
                )

            # Convert list back to single str
            number_to_base = "".join(number_to_base_as_list)

        logger.info(f"Converted number: {number_to_base}")
        return number_to_base

    @staticmethod
    def _increment_by_one(number_as_list, base):
        # Maps from and to decimal
        inv_supported_digits = {
            value: key for key, value in SUPPORTED_DIGITS.items()
        }
        inv_valid_digits_and_stop = {
            key: inv_supported_digits[key] for key in range(base)
        }
        inv_valid_digits_and_stop[base] = STOP_SYMBOL
        valid_digits_and_stop = {
            value: key for key, value in inv_valid_digits_and_stop.items()
        }

        # Convert from little to big endian
        be_number_as_list = list(reversed(number_as_list))

        # Increment the least significant digit
        # i.e., the 1st one since we switched to big endian
        be_number_as_list[0] = inv_valid_digits_and_stop[
            valid_digits_and_stop[be_number_as_list[0]] + 1
        ]

        # As long as there's a stop symbol, carry over
        while STOP_SYMBOL in be_number_as_list:
            stop_idx = [
                idx
                for idx, value in enumerate(be_number_as_list)
                if value == STOP_SYMBOL
            ][0]
            be_number_as_list[stop_idx] = inv_supported_digits[0]
            if stop_idx + 2 > len(be_number_as_list):
                be_number_as_list.append(inv_supported_digits[1])
            else:
                be_number_as_list[stop_idx + 1] = inv_valid_digits_and_stop[
                    valid_digits_and_stop[be_number_as_list[stop_idx + 1]] + 1
                ]

        # Switch back to little endian
        number_as_list = list(reversed(be_number_as_list))

        return number_as_list


def convert_number(number: str, from_base: int, to_base: int) -> str:
    """
    Convert a number from one positional numeral system to another.

    :param number: str - number to be converted
    :param from_base: int - base of the provided number
    :param to_base: int - base to convert the number to
    """

    return Number(number, base=from_base).to_base(to_base)
