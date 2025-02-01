import random
from math import gcd

# Teste de primalidade Miller-Rabin
def miller_rabin(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Escreve n-1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

# Geração de primos grandes
def generate_large_prime(bits):
    while True:
        prime = random.getrandbits(bits)
        prime |= (1 << bits - 1) | 1  # Garante que tem exatamente 'bits' bits e é ímpar
        if miller_rabin(prime):
            return prime

# Geração de chaves RSA
def generate_keys(bits=1024):
    while True:
        print("Gerando p...")
        p = generate_large_prime(bits)
        print(f'P gerado com {bits} bits')

        print("Gerando q...")
        q = generate_large_prime(bits)
        print(f'Q gerado com {bits} bits')

        if p == q:
            print("Primos iguais, gerando novamente...")
            continue  # Garante que p e q são diferentes

        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537
        if gcd(e, phi) == 1:  # Apenas seguimos se e for coprimo de φ(n)
            break

    # Calcula d (inverso modular de e mod phi)
    d = pow(e, -1, phi)

    return (e, n), (d, n)
