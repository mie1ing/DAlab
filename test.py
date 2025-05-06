import math

def is_prime(n):
    if n < 2:
        return False
    # check if n is divisible by any number in range 2...√(n) (rounded up)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def test_is_prime():
    assert is_prime(1) == False
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False

test_is_prime()