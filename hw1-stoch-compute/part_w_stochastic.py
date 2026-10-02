import numpy as np

class BipolarStochasticComputing:
    @classmethod
    def to_stoch(cls, val, nbits):
        assert -1.0 <= val <= 1.0
        prob = (val + 1.0) / 2.0
        return np.random.binomial(1, prob, size=nbits)

    @classmethod
    def stoch_add(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))

        return np.where(
            np.random.randint(0, 2, size=len(bitstream)),
            bitstream,
            bitstream2
        )

    @classmethod
    def stoch_mul(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))

        return 1 - np.logical_xor(bitstream, bitstream2).astype(int)

    @classmethod
    def from_stoch(cls, result):
        return 2.0 * np.mean(result) - 1.0
