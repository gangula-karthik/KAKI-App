import scrypt
import os

def hash_value(value):
    algorithm = scrypt.params(alg=scrypt.SCRYPT_SALSA256_SHA256,
                              saltsep=b'Bw==',
                              N=2**8,  # Number of rounds (2^8 = 256 rounds)
                              r=8,     # Block size
                              p=1,     # Parallelization factor
                              buflen=64)  # Desired key length
    
    base64_signer_key = b"6/AWTKOmeoDnlqUMybnu3XVSNWeYuXJWioqrseNMlQDDiikwJcLqUXBrQjDnWHP2CRpb4ap/6/4kVawp7VLKnA=="
    signer_key = scrypt.decode_base64(base64_signer_key)
    
    salt = os.urandom(16)  # Generate a random 16-byte salt (adjust size as needed)
    
    # Hash the value using scrypt
    hashed_value = scrypt.hash(value.encode('utf-8'), salt, N=algorithm.N, r=algorithm.r, p=algorithm.p, buflen=algorithm.buflen, key=signer_key)
    
    return hashed_value

# Example usage:
value_to_hash = "test123"
hashed_value = hash_value(value_to_hash)
print("Hashed value:", hashed_value.hex())