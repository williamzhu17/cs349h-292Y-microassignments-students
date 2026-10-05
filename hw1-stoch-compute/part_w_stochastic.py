import numpy as np

# TODO: fill these in after training on software
NETWORK_PARAMS = {}

# Params used for initial testing
TEST_PARAMS = {
    "W": np.array([[0.8, 0.8], [-0.8, -0.8]]),
    "b": np.array([-0.8, -0.8]),
    "v": np.array([-0.8, -0.8]),
    "b_o": -0.8,
}

XOR_EXAMPLES = [
    (np.array([-0.8, -0.8]), 0),
    (np.array([-0.8, +0.8]), 1),
    (np.array([+0.8, -0.8]), 1),
    (np.array([+0.8, +0.8]), 0),
]

COUNTER_MAX = 7
COUNTER_THRESHOLD = 4
COUNTER_INIT = 4

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
    def stoch_add4(cls, a, b, c, d):
        first_half = cls.stoch_add(a, b)
        second_half = cls.stoch_add(c, d)

        return cls.stoch_add(first_half, second_half)

    @classmethod
    def stoch_mul(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))

        return 1 - np.logical_xor(bitstream, bitstream2).astype(int)

    @classmethod
    def from_stoch(cls, result):
        return 2.0 * np.mean(result) - 1.0

    @classmethod
    def saturating_counter(cls, bitstream, initial_count=COUNTER_INIT):
        count = initial_count
        out_stream = np.empty(len(bitstream), dtype=int)

        for i, bit in enumerate(bitstream):
            count = min(COUNTER_MAX, count + 1) if bit else max(0, count - 1)
            out_stream[i] = 1 if count >= COUNTER_THRESHOLD else 0

        return out_stream

def ideal_forward(x, params):
    W, b, v, b_o = params["W"], params["b"], params["v"], params["b_o"]

    h = np.tanh(4.0 * (W @ x + b) / 4.0)
    s = (np.dot(v, h) + b_o) / 4.0
    pred = 1 if s > 0 else 0

    return pred, s

def stoch_forward(x, params, n):
    BSC = BipolarStochasticComputing

    W, b, v, b_o = params["W"], params["b"], params["v"], params["b_o"]

    x0 = BSC.to_stoch(float(x[0]), n)
    x1 = BSC.to_stoch(float(x[1]), n)

    h_bits = []

    # For two neurons
    for i in range(2):
        # Weight * x input
        p0 = BSC.stoch_mul(x0, BSC.to_stoch(float(W[i, 0]), n))
        p1 = BSC.stoch_mul(x1, BSC.to_stoch(float(W[i, 1]), n))

        # Add bias
        bias = BSC.to_stoch(float(b[i]), n)
        zero = BSC.to_stoch(0.0, n)
        preact = BSC.stoch_add4(p0, p1, bias, zero)

        # tanh
        postact = BSC.saturating_counter(preact)

        # Set h_bits
        h_bits.append(postact)

    # Multiply with output weights
    o0 = BSC.stoch_mul(h_bits[0], BSC.to_stoch(float(v[0]), n))
    o1 = BSC.stoch_mul(h_bits[1], BSC.to_stoch(float(v[1]), n))
    
    # Add output bias
    out = BSC.stoch_add4(o0, o1, BSC.to_stoch(float(b_o), n), BSC.to_stoch(0.0, n))

    s = BSC.from_stoch(out)
    pred = 1 if s > 0 else 0

    return pred, s

if __name__ == "__main__":
    params = TEST_PARAMS

    print("ideal:")
    for x, label in XOR_EXAMPLES:
        pred, s = ideal_forward(x, params)
        print(f"  x=({x[0]:+.1f},{x[1]:+.1f}) label={label}  s={s:+.4f} pred={pred}")

    for n in (64, 128, 256, 512, 1024):
        print(f"\nnbits={n}")
        for x, label in XOR_EXAMPLES:
            pred, s = stoch_forward(x, params, n)
            print(f"  x=({x[0]:+.1f},{x[1]:+.1f}) label={label}  s={s:+.4f} pred={pred}")
