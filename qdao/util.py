BITS = [
    1,
    2,
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
    131072,
    262144,
    524288,
    1048576,
    2097152,
    4194304,
    8388608,
    16777216,
    33554432,
    67108864,
    134217728,
    268435456,
    536870912,
    1073741824,
    2147483648,
    4294967296,
    8589934592,
    17179869184,
    34359738368,
    68719476736,
    137438953472,
    274877906944,
    549755813888,
    1099511627776,
    2199023255552,
    4398046511104,
    8796093022208,
    17592186044416,
    35184372088832,
    70368744177664,
    140737488355328,
    281474976710656,
    562949953421312,
    1125899906842624,
    2251799813685248,
    4503599627370496,
    9007199254740992,
    18014398509481984,
    36028797018963968,
    72057594037927936,
    144115188075855872,
    288230376151711744,
    576460752303423488,
    1152921504606846976,
    2305843009213693952,
    4611686018427387904,
    9223372036854775808,
]

MASKS = [
    0,
    1,
    3,
    7,
    15,
    31,
    63,
    127,
    255,
    511,
    1023,
    2047,
    4095,
    8191,
    16383,
    32767,
    65535,
    131071,
    262143,
    524287,
    1048575,
    2097151,
    4194303,
    8388607,
    16777215,
    33554431,
    67108863,
    134217727,
    268435455,
    536870911,
    1073741823,
    2147483647,
    4294967295,
    8589934591,
    17179869183,
    34359738367,
    68719476735,
    137438953471,
    274877906943,
    549755813887,
    1099511627775,
    2199023255551,
    4398046511103,
    8796093022207,
    17592186044415,
    35184372088831,
    70368744177663,
    140737488355327,
    281474976710655,
    562949953421311,
    1125899906842623,
    2251799813685247,
    4503599627370495,
    9007199254740991,
    18014398509481983,
    36028797018963967,
    72057594037927935,
    144115188075855871,
    288230376151711743,
    576460752303423487,
    1152921504606846975,
    2305843009213693951,
    4611686018427387903,
    9223372036854775807,
]

DATA_DIR = "data"
SECONDARY_PREFIX = "sv"
SECONDARY_SUFFIX = ".npy"


def generate_secondary_file_name(idx: int):
    return DATA_DIR + "/" + SECONDARY_PREFIX + str(idx) + SECONDARY_SUFFIX


def index0(qubits, k):
    """
    Used to find the start entry of an single matrix-vector multiplication
    E.g., an op is operating on qubit 0 and 2
     The indexes of states are as follows
     00000
     00001
     00010
     00011
     00100
     00101
     00110
     00111
     So the frist group is 00000,00001,00100,00101, we can see that the start
     is 00000, which is inserting 0 at index 0 and 2. Similarly the second group's
     start is 00010, which is inserting 0 at index 0 and 2 to 1
    Therefore, find the kth group's start is inserting 0 to k based on qubits.
    The algorithm works as follows
     1. A binary abcde, we want to add 0 to position 1, then it becomes abcd0e
     2. First, get e (i.e., the lowbits)
     3. Second, get abcd00 (i.e., abcde >>= 1 (abcd) and then <<= 2 (abcd00))
     4. Third, add lowbits using | (i.e., abcd00 | e = abcd0e)
    Reference:
     https://github.com/Qiskit/qiskit-aer/blob/main/src/simulators/statevector/indexes.hpp#L121

    Args:
        qubits (List): the qubits that are acted on
        k (int): the k-th group of state vectors that are operated on

    Returns:
        int: the first index of the k-th group of elements

    """
    lowbits = 0
    retval = k

    for j in range(len(qubits)):
        lowbits = retval & MASKS[qubits[j]]
        # Start: insert zero and make all lowbits zero
        retval >>= qubits[j]
        retval <<= qubits[j] + 1
        # End
        retval |= lowbits

    return retval


def indexes(qubits, k):
    """
    Get the indexes that an op operate on
    E.g.,
          qubits = [1, 3], k = 0, ==> [00000,00010,01000,01010]
                           k = 1, ==> [00001,00011,01001,01011]

          qubits = [0, 2, 3], k = 0
            ==> [00000000, 00000001, 00000100, 00000101
                 00001000, 00001001, 00001100, 00001101]
            k = 1
            ==> [00000010, 00000011, 00000110, 00000111
                 00001010, 00001011, 00001110, 00001111]
            k = 2
            ==> [00010000, 00010001, 00010100, 00010101
                 00011000, 00011001, 00011100, 00011101]
    Explanation: TODO: Add doc link

    Args:
        qubits (List): the qubits that are acted on
        k (int): the k-th group of state vectors that are operated on

    Returns:
        list[int]: List of indexes of k-th state group
    """
    num_qubits = len(qubits)
    num_indexes = BITS[num_qubits]
    ret = list()
    for i in range(num_indexes):
        if i == 0:
            ret.append(index0(qubits, k))
        else:
            ret.append(0)

    for i in range(num_qubits):
        # `n`: number of states
        # that can be deduced from previous half
        n = BITS[i]
        # `bias`: index pattern repeat from bias + start
        bias = BITS[qubits[i]]
        for j in range(n):
            ret[n + j] = ret[j] | bias

    return ret


def retrieve_sv(num_qubits: int, num_local: int = 2):
    """Retrieve statevector from disk

    This is used only for test, and must be used after simulation finished

    Args:
        num_qubits (int): Number of qubits
        num_local (int): Number of qubits stored in single storage unit
    """
    import numpy as np

    # Calculate the number of storage units
    num_sus = 1 << (num_qubits - num_local)
    su_size = 1 << num_local
    sv = np.zeros(1 << num_qubits, dtype=complex)

    for i in range(num_sus):
        fn = generate_secondary_file_name(i)
        vec = np.load(fn)
        sv[i * su_size : (i + 1) * su_size] = vec

    return sv


def safe_import(module_name, submodule_name):
    """Import a sumodule from a module, if the module is
    not installed, no error occurs

    Args:
        module_name: The name of module.
        submodule_name: The name of submodule in the module

    Notes:
        Currently only support decorator
    """
    try:
        module = __import__(module_name)
        return getattr(module, submodule_name)
    except ImportError as ex:

        def placeholder_decorator(func):
            return func

        return placeholder_decorator
