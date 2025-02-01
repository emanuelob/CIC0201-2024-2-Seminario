from key_generator import generate_keys
from RPA_OAEP import rsa_encrypt, rsa_decrypt

# Separador para melhor visualização
print("\n" + "="*40)
print("TESTE: Cifração e Decifração RSA-OAEP")
print("="*40)

# Geração de chaves (pode ser 1024 ou 2048 bits para mais segurança)
print("\nGerando chaves RSA...")
public_key, private_key = generate_keys(1024)

# Mensagem de teste
mensagem = b"Teste RSA OAEP"
print("\nMensagem original:", mensagem.hex())

try:
    # Cifração
    print("\nCifrando a mensagem...")
    ciphertext = rsa_encrypt(public_key, mensagem)
    print("Texto cifrado:", ciphertext.hex())

    # Decifração
    print("\nDecifrando a mensagem...")
    plaintext = rsa_decrypt(private_key, ciphertext)
    print("Texto decifrado (hex):", plaintext.hex())
    print("Texto decifrado (string):", plaintext.decode())

    # Verificação de integridade
    assert mensagem == plaintext, "Erro: Mensagem decifrada não corresponde!"
    print("\n✅ Teste concluído com sucesso!")

except Exception as e:
    print("\n❌ Erro durante o teste:", e)
