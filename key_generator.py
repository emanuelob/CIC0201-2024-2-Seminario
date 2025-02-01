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
    print("Gerando número primo p...")
    p = generate_large_prime(bits)
    print(f"P gerado: {p} ({bits} bits)")

    print("Gerando número primo q...")
    q = generate_large_prime(bits)
    while p == q:  # Garante que p e q são diferentes
        print("Primos iguais, gerando um novo q...")
        q = generate_large_prime(bits)
    print(f"Q gerado: {q} ({bits} bits)")

    n = p * q
    phi = (p - 1) * (q - 1)
    print(f"Modulus n = p * q: {n}")
    print(f"Totiente de Euler φ(n): {phi}")

    e = 65537
    while gcd(e, phi) != 1:  # Se não for coprimo, escolha outro `e`
        print(f"e={e} não é coprimo com φ(n), escolhendo outro valor...")
        e = random.randint(2, phi - 1)

    print(f"Expoente público escolhido: e={e}")

    d = pow(e, -1, phi)  # Calcula d como o inverso modular de e
    print(f"Expoente privado calculado: d={d}")

    return (e, n), (d, n)
