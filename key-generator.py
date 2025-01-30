import random
import hashlib
from math import gcd

# Função auxiliar para teste de primalidade usando Miller-Rabin
def miller_rabin(n, k=40):  # Teste de primalidade probabilística
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

# Geração de números primos grandes
def generate_large_prime(bits):
    while True:
        prime = random.getrandbits(bits)
        prime |= (1 << bits - 1) | 1  # Garante que o número tem o tamanho correto e é ímpar
        if miller_rabin(prime):
            return prime

# Geração de chaves RSA
def generate_keys(bits=1024):
    print("Gerando p...")
    p = generate_large_prime(bits)
    print(f'P = {p} \nTamanho q = {len(str(p))}')
    print("Gerando q...")
    q = generate_large_prime(bits)
    print(f'Q = {q} \nTamanho q = {len(str(q))}')

    n = p * q
    phi = (p - 1) * (q - 1)

    # Escolha de e
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Cálculo de d
    d = pow(e, -1, phi)

    return (e, n), (d, n)


print("Gerando chaves RSA...")
public_key, private_key = generate_keys(1024)

print("Chave Pública:", public_key)
print("Chave Privada:", private_key)