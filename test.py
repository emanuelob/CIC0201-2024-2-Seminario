from key_generator import generate_keys
from RPA_OAEP import rsa_encrypt, rsa_decrypt

# Geração de chaves
public_key, private_key = generate_keys(1024)

# Mensagem de teste
mensagem = b"Teste RSA OAEP"
print("Mensagem original:", mensagem.hex())

# Cifração
ciphertext = rsa_encrypt(public_key, mensagem)
print("Texto cifrado:", ciphertext.hex())

# Decifração
plaintext = rsa_decrypt(private_key, ciphertext)
print("Texto decifrado:", plaintext.hex())
print("Texto decifrado:", plaintext.decode()) 

