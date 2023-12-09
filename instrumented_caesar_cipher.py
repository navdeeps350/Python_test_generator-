from instrumentor import evaluate_condition 



def decrypt_instrumented(strng: str, key: int) -> str:
    assert 0 < key <= 94
    decrypted = ''
    for x in strng:
        indx = (ord(x) - key) % 256
        if evaluate_condition(1, 'Lt', indx, 32):
            indx = indx + 95
        decrypted = decrypted + chr(indx)
    return decrypted

def encrypt_instrumented(strng: str, key: int) -> str:
    assert 0 < key <= 94
    encrypted = ''
    for x in strng:
        indx = (ord(x) + key) % 256
        if evaluate_condition(2, 'Gt', indx, 126):
            indx = indx - 95
        encrypted = encrypted + chr(indx)
    return encrypted