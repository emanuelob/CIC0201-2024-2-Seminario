import hashlib
import base64
import json
from RPA_OAEP import rsa_encrypt, rsa_decrypt

# Função para calcular o hash da mensagem usando SHA-3
def calculate_hash(message, hash_func=hashlib.sha3_256):
    """ Calcula o hash SHA-3 da mensagem """
    return hash_func(message).digest()

# Função para assinar uma mensagem
def sign_message(private_key, message):
    """ Assina uma mensagem cifrando seu hash com a chave privada """
    hash_value = calculate_hash(message)
    signature = rsa_encrypt(private_key, hash_value)  # Cifra o hash com RSA

    # Codifica a assinatura em Base64
    signature_b64 = base64.b64encode(signature).decode()

    # Obtém o tamanho da chave (número de bits do módulo n)
    key_size = private_key[1].bit_length()

    # Formatação do resultado em JSON
    signature_json = json.dumps({
        "algorithm": "SHA3-256",
        "key_size": key_size,
        "signature": signature_b64
    })

    return signature_json  # Retorna assinatura formatada como JSON

# Função para verificar uma assinatura
def verify_signature(public_key, message, signature_json):
    """ Verifica uma assinatura decifrando e comparando os hashes """
    
    # Carregar assinatura a partir do JSON
    try:
        signature_data = json.loads(signature_json)
        signature_b64 = signature_data["signature"]
    except (json.JSONDecodeError, KeyError):
        raise ValueError("Formato de assinatura inválido")

    # Decodifica assinatura Base64
    signature = base64.b64decode(signature_b64)

    # Decifra a assinatura (obtemos o hash original)
    decrypted_hash = rsa_decrypt(public_key, signature)

    # Calcula o hash da mensagem original
    expected_hash = calculate_hash(message)

    # Retorna True se os hashes forem iguais, caso contrário False
    return decrypted_hash == expected_hash
