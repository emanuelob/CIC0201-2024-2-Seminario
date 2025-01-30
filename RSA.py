# Função MGF1
def mgf1(seed, mask_len, hash_func=hashlib.sha256):
    hlen = hash_func().digest_size
    if mask_len > (2 ** 32) * hlen:
        raise ValueError("Máscara muito longa.")

    t = b""
    for i in range((mask_len + hlen - 1) // hlen):
        c = i.to_bytes(4, 'big')
        t += hash_func(seed + c).digest()

    return t[:mask_len]

# Cifração RSA
def rsa_encrypt(message, public_key):
    e, n = public_key
    encoded = oaep_encode(message, n)
    m = int.from_bytes(encoded, 'big')
    c = pow(m, e, n)
    return c

# Decifração RSA
def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    encoded = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    return oaep_decode(encoded, n)

# Exemplo de uso
if __name__ == "__main__":
    print("Gerando chaves RSA...")
    public_key, private_key = generate_keys(1024)

    print("Chave Pública:", public_key)
    print("Chave Privada:", private_key)

    mensagem = b"Mensagem secreta!"
    print("\nCifrando mensagem...")
    cifra = rsa_encrypt(mensagem, public_key)
    print("Cifra:", cifra)

    print("\nDecifrando mensagem...")
    decifrada = rsa_decrypt(cifra, private_key)
    print("Mensagem decifrada:", decifrada)

    # Teste adicional com mensagens curtas
    mensagem_teste = b"Teste"
    print("\nTeste com mensagem curta...")
    cifra_teste = rsa_encrypt(mensagem_teste, public_key)
    mensagem_decifrada = rsa_decrypt(cifra_teste, private_key)
    assert mensagem_teste == mensagem_decifrada, "Erro na decifração da mensagem curta!"
    print("Teste bem-sucedido com mensagem curta.")