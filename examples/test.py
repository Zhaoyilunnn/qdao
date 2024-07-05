
from test1 import divide, communication


if __name__ == "__main__":
    variable_to_share = divide()
    communication(variable_to_share)
    a = [0, 2, 0, 2]
    print(list(set(a)))
