import random
import hashlib

# Função para converter um inteiro em uma string de octetos (I2OSP)
def i2osp(x, l):
    """ Converte um inteiro x em uma string de octetos de comprimento l """
    if x >= 256**l:
        raise ValueError("Inteiro muito grande")
    return x.to_bytes(l, byteorder='big')

# Função para converter uma string de octetos em um inteiro (OS2IP)
def os2ip(X):
    """ Converte uma string de octetos X em um inteiro """
    return int.from_bytes(X, byteorder='big')

# Função de Geração de Máscara (MGF1) usada no esquema OAEP
def mgf1(seed, length, hash_func=hashlib.sha3_256):
    """ Gera uma máscara de comprimento especificado a partir de um seed """
    hLen = hash_func().digest_size
    T = b''
    for i in range((length + hLen - 1) // hLen):
        C = i2osp(i, 4)
        T += hash_func(seed + C).digest()
    return T[:length]

# Codificação OAEP
def oaep_encode(message, label, k, hash_func=hashlib.sha3_256):
    """ Aplica o esquema de padding OAEP a uma mensagem """
    hLen = hash_func().digest_size
    mLen = len(message)
    
    if mLen > k - 2 * hLen - 2:
        raise ValueError("Mensagem muito longa")
    
    lHash = hash_func(label).digest()
    PS = b'\x00' * (k - mLen - 2 * hLen - 2)
    DB = lHash + PS + b'\x01' + message
    seed = random.randbytes(hLen)
    dbMask = mgf1(seed, k - hLen - 1, hash_func)
    maskedDB = bytes(x ^ y for x, y in zip(DB, dbMask))
    seedMask = mgf1(maskedDB, hLen, hash_func)
    maskedSeed = bytes(x ^ y for x, y in zip(seed, seedMask))
    
    print("Seed:", seed.hex())
    print("DB:", DB.hex())
    print("Masked DB:", maskedDB.hex())
    
    return b'\x00' + maskedSeed + maskedDB

# Decodificação OAEP
def oaep_decode(encoded_message, label, k, hash_func=hashlib.sha3_256):
    """ Decodifica uma mensagem formatada com OAEP """
    hLen = hash_func().digest_size
    if len(encoded_message) != k:
        raise ValueError("Erro na decodificação")
    
    maskedSeed = encoded_message[1:hLen+1]
    maskedDB = encoded_message[hLen+1:]
    seedMask = mgf1(maskedDB, hLen, hash_func)
    seed = bytes(x ^ y for x, y in zip(maskedSeed, seedMask))
    dbMask = mgf1(seed, k - hLen - 1, hash_func)
    DB = bytes(x ^ y for x, y in zip(maskedDB, dbMask))
    
    lHash = hash_func(label).digest()
    if DB[:hLen] != lHash:
        raise ValueError("Erro na decodificação")
    
    i = hLen
    while i < len(DB) and DB[i] == 0:
        i += 1
    if DB[i] != 1:
        raise ValueError("Erro na decodificação")
    
    mensagem_decodificada = DB[i+1:]
    print("Mensagem decodificada:", mensagem_decodificada.hex())
    return mensagem_decodificada

# Cifração RSA com OAEP
def rsa_encrypt(public_key, message, label=b"", hash_func=hashlib.sha3_256):
    """ Cifra uma mensagem utilizando RSA e OAEP """
    e, n = public_key
    k = (n.bit_length() + 7) // 8
    encoded_message = oaep_encode(message, label, k, hash_func)
    m = os2ip(encoded_message)
    c = pow(m, e, n)
    
    print("Mensagem codificada (inteiro):", m)
    print("Texto cifrado (inteiro):", c)
    
    return i2osp(c, k)

# Decifração RSA com OAEP
def rsa_decrypt(private_key, ciphertext, label=b"", hash_func=hashlib.sha3_256):
    """ Decifra um texto cifrado utilizando RSA e OAEP """
    d, n = private_key
    k = (n.bit_length() + 7) // 8
    c = os2ip(ciphertext)
    m = pow(c, d, n)
    encoded_message = i2osp(m, k)
    
    print("Texto decifrado (inteiro):", m)
    
    return oaep_decode(encoded_message, label, k, hash_func)