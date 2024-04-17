import decimal


class NumberConverter:
    def __init__(self):
        self.UNDER_20 = [
            "Zero",
            "One",
            "Two",
            "Three",
            "Four",
            "Five",
            "Six",
            "Seven",
            "Eight",
            "Nine",
            "Ten",
            "Eleven",
            "Twelve",
            "Thirteen",
            "Fourteen",
            "Fifteen",
            "Sixteen",
            "Seventeen",
            "Eighteen",
            "Nineteen",
        ]
        self.TENS = [
            "Twenty",
            "Thirty",
            "Forty",
            "Fifty",
            "Sixty",
            "Seventy",
            "Eighty",
            "Ninety",
        ]
        self.ABOVE_100 = {
            100: "Hundred",
            1000: "Thousand",
            100000: "Lakhs",
            10000000: "Crores",
        }

    def _convert_decimal(self, number, decimal_part):
        return (
            self.to_words(number)
            + " point "
            + "".join(self.to_words(int(i)) for i in str(decimal_part)[2:])
        )

    def to_words(self, number):
        target_number = decimal.Decimal(number)
        decimal_part = target_number - int(target_number)
        target_number = int(target_number)

        if decimal_part:
            return self._convert_decimal(target_number, decimal_part)
        elif target_number < 20:
            return self.UNDER_20[target_number]
        elif target_number < 100:
            quotient, remainder = divmod(number, 10)
            return self.TENS[quotient - 2] + (
                "" if remainder == 0 else " " + self.UNDER_20[remainder]
            )
        else:
            pivot = max(key for key in self.ABOVE_100 if key <= number)
            quotient, remainder = divmod(number, pivot)

            return (
                self.to_words(quotient)
                + " "
                + self.ABOVE_100[pivot]
                + ("" if remainder == 0 else " " + self.to_words(remainder))
            )
