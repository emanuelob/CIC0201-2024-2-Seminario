# Padding OAEP
def oaep_encode(message, n):
    k = (n.bit_length() + 7) // 8  # Tamanho do módulo em bytes
    hash_len = hashlib.sha256().digest_size
    ps_len = k - len(message) - 2 * hash_len - 2

    if ps_len < 0:
        raise ValueError("Mensagem muito longa.")

    ps = b"\x00" * ps_len
    db = hashlib.sha256(b"").digest() + ps + b"\x01" + message
    seed = random.randbytes(hash_len)
    db_mask = mgf1(seed, len(db))
    masked_db = bytes(x ^ y for x, y in zip(db, db_mask))
    seed_mask = mgf1(masked_db, len(seed))
    masked_seed = bytes(x ^ y for x, y in zip(seed, seed_mask))

    encoded = b"\x00" + masked_seed + masked_db
    print(f"OAEP Encode: Tamanho k={k}, Hash Len={hash_len}, PS Len={ps_len}")
    print(f"Seed: {seed.hex()}, Masked Seed: {masked_seed.hex()}")
    print(f"DB: {db.hex()}, Masked DB: {masked_db.hex()}")
    return encoded

def oaep_decode(encoded, n):
    k = (n.bit_length() + 7) // 8
    hash_len = hashlib.sha256().digest_size
    print(f"{len(encoded)} {k}")
    print(f"{encoded[0]}")
    
    if len(encoded) != k or encoded[0] != 0:
        raise ValueError("Formato inválido: comprimento incorreto ou byte inicial inválido.")

    masked_seed = encoded[1:1 + hash_len]
    masked_db = encoded[1 + hash_len:]
    seed_mask = mgf1(masked_db, len(masked_seed))
    seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))
    db_mask = mgf1(seed, len(masked_db))
    db = bytes(x ^ y for x, y in zip(masked_db, db_mask))

    l_hash = hashlib.sha256(b"").digest()
    print(f"OAEP Decode: Masked Seed: {masked_seed.hex()}, Seed: {seed.hex()}")
    print(f"Masked DB: {masked_db.hex()}, DB: {db.hex()}")
    if db[:hash_len] != l_hash:
        raise ValueError("Hash inconsistente no DB.")

    try:
        i = db.index(b"\x01", hash_len)
    except ValueError:
        raise ValueError("Delimitador '\x01' não encontrado no DB.")

    message = db[i + 1:]
    print(f"Mensagem decodificada: {message}")
    return message
 