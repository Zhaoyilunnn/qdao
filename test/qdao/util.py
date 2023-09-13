import sys

sys.path.append("/root/projects/qcs")

from qdao.util import indexes

# 00000010
# 00001010
# 00100010
# 00101010
# 10000010
# 10001010
# 10100010
# 10101010
test_cases = [
    ([1, 2], 0, [0, 2, 4, 6]),
    ([3], 3, [3, 11]),
    ([3, 5, 7], 2, [2, 10, 34, 42, 130, 138, 162, 170]),
    ([0, 2, 3], 2, [16, 17, 20, 21, 24, 25, 28, 29]),
]


class TestQdaoUtil:
    def test_indexes(self):
        for case in test_cases:
            assert indexes(case[0], case[1]) == case[2]
