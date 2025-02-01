from key_generator import generate_keys
from signature import sign_message, verify_signature

# Separador para melhor visualização
print("\n" + "="*40)
print("TESTE: Assinatura Digital RSA")
print("="*40)

# Gerando chaves RSA
print("\nGerando chaves RSA...")
public_key, private_key = generate_keys(1024)

# Mensagem de teste
message = b"Mensagem para assinatura digital"
print("\nMensagem original:", message.decode())

# Criando assinatura
print("\nGerando assinatura...")
signature = sign_message(private_key, message)
print("Assinatura gerada (Base64):", signature)

# Verificando assinatura
print("\nVerificando assinatura...")
is_valid = verify_signature(public_key, message, signature)
print("Assinatura válida?" , "✅ Sim" if is_valid else "❌ Não")

# Teste com mensagem alterada
altered_message = b"Mensagem alterada"
print("\nVerificando assinatura em mensagem alterada...")
is_valid_altered = verify_signature(public_key, altered_message, signature)
print("Assinatura válida para mensagem alterada?", "✅ Sim" if is_valid_altered else "❌ Não")
