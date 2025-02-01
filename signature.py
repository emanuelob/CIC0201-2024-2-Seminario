import hashlib
import base64
from RPA_OAEP import rsa_encrypt, rsa_decrypt
from key_generator import generate_keys

# Função para calcular o hash SHA-3 da mensagem
def calculate_hash(message, hash_func=hashlib.sha3_256):
    """ Calcula o hash SHA-3 da mensagem """
    return hash_func(message).digest()

# Função para assinar uma mensagem (cifrando o hash com RSA)
def sign_message(private_key, message):
    """ Assina uma mensagem cifrando seu hash com RSA """
    hash_value = calculate_hash(message)
    signature = rsa_encrypt(private_key, hash_value)
    return base64.b64encode(signature).decode()

# Função para verificar a assinatura
def verify_signature(public_key, message, signature_b64):
    """ Verifica uma assinatura decifrando e comparando os hashes """
    signature = base64.b64decode(signature_b64)
    decrypted_hash = rsa_decrypt(public_key, signature)
    expected_hash = calculate_hash(message)
    
    return decrypted_hash == expected_hash
