import random


class CDMA:
    """
    Implementation of the Code Division Multiple Access Protocol
    """

    @staticmethod
    def text_to_bits(text):
        """
        Converts a string of text to a list of bits.
        """
        bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
        return list(map(int, bits.zfill(8 * ((len(bits) + 7) // 8))))

    @staticmethod
    def text_from_bits(bits):
        """
        Converts a list of bits to a string of text.
        """
        n = int(''.join(map(str, bits)), 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    @staticmethod
    def to_bit(volt):
        """
        Converts a volt into a bit.
        """
        if volt == 1:
            return 0
        else:
            return 1

    @staticmethod
    def to_volts(bit):
        """
        Converts a bit into a volt.
        """
        if bit == 0:
            return 1
        else:
            return -1

    def xor(self, bit1, bit2):
        """
        Performs the XOR operation on two bits and returns the result.
        """
        if bit1 == 0:
            if bit2 == 0:
                return 0
            if bit2 == 1:
                return 1
        if bit2 == 0:
            if bit1 == 1:
                return 1
        if bit2 == 1:
            if bit1 == 1:
                return 0

    def create_code(self, len_code):
        """
        Creates a code given a code length
        """
        code = []
        for i in range(0, len_code):
            num = random.randint(0, 1)
            code.append(num)
        return code

    def is_orthogonal(self, tmp_code, code):
        """
        Checks if two codes, tmp_code and code are orthogonal with each other.
        """
        tmp_volt = []
        code_volt = []
        result_volt = []
        result = 0
        for bit in tmp_code:
            tmp_volt.append(self.to_volts(bit))
        for bit in code:
            code_volt.append(self.to_volts(bit))
        for i in range(len(code_volt)):
            result_volt.append(tmp_volt[i] * code_volt[i])
        for i in range(len(result_volt)):
            result = result + result_volt[i]
        if result == 0:
            return True
        else:
            return False

    def codes(self, number_users, len_code):  #length of code is data length * 2
        """
        Creates orthogonal codes based on the number of users and the length of the codes.
        Will return an array of orthogonal codes for each user.
        """
        codes = []
        count = 0
        first_code = self.create_code(len_code)
        codes.append(first_code)
        tmp_code = None
        for i in range(number_users - 1):
            while True:
                count = 0
                tmp_code = self.create_code(len_code)
                for code in codes:
                    if self.is_orthogonal(tmp_code, code):
                        count = count + 1
                if count == len(codes):
                    break
            codes.append(tmp_code)
        return codes

    def encode(self, data, code):
        """
        Encodes the data for one of the users using the code. Returns an array
        of encoded data.
        """
        encoded = []
        doubledata = []
        tmp_code = []

        for i in range(len(data)):
            codelen = len(code)
            while codelen > 0:
                doubledata.append(data[i])
                codelen = codelen - 1
        while len(tmp_code) != len(doubledata):
            tmp_code.extend(code)
        for i in range(0, len(doubledata)):
            result = self.xor(doubledata[i], tmp_code[i])  # perform XOR
            encoded.append(result)
        return encoded

    def encode_all(self, encoded_data):
        """
        Puts all the frequencies together and returns the one frequency
        where all the data from all the users are encoded.
        """
        index = 0
        frequency = [0] * len(encoded_data[0])  # creating list of len encoded data and initialize with 0
        for data in encoded_data:
            index = 0
            for i in data:
                volt = self.to_volts(i)
                data[index] = volt
                index = index + 1
            for x in range(len(data)):
                frequency[x] += data[x]
        return frequency

    def decode(self, frequency, code):
        """
        Decodes and returns the data in a list of bits.
        """
        data = []
        tmp_code = []
        bits = []

        while len(tmp_code) != len(frequency):
            tmp_code.extend(code)
        volt_code = []
        for bit in tmp_code:            # make code into volts
            volt_code.append(self.to_volts(bit))
        # code = self.to_volts(code)
        len_code = len(code)
        code_index = 0
        volt_code_index = 0
        sum_volts = 0
        for volt in frequency:
            if volt_code_index == len_code:
                data.append(sum_volts)
                volt_code_index = 0
                sum_volts = 0

            result = volt * volt_code[volt_code_index]
            sum_volts += result
            volt_code_index = volt_code_index + 1
        data.append(sum_volts)
        for volt in data:
            bits.append(self.to_bit(int(volt/(len(code)))))
        return bits
