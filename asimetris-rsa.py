import random

# Fungsi cek bilangan prima
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Fungsi menghasilkan semua bilangan prima dalam rentang
def primes_in_range(start, end):
    primes = []
    for num in range(start, end+1):
        if is_prime(num):
            primes.append(num)
    return primes

# Extended Euclidean Algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

# Fungsi invers modular
def modinv(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Tidak ada invers modular")
    return x % phi

# Modular exponentiation
def modexp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

# Generate kunci RSA dari p dan q yang dipilih
def generate_keys(p, q):
    n = p * q
    phi = (p-1)*(q-1)
    
    e = 3
    while True:
        gcd, _, _ = extended_gcd(e, phi)
        if gcd == 1:
            break
        e += 2
    
    d = modinv(e, phi)
    return (e, n), (d, n)

# Fungsi enkripsi
def encrypt(msg, public):
    e, n = public
    return [modexp(ord(c), e, n) for c in msg]

# Fungsi dekripsi
def decrypt(cipher, private):
    d, n = private
    return ''.join([chr(modexp(c, d, n)) for c in cipher])

# Fungsi konversi ciphertext ke kode ASCII
def cipher_ascii_codes(cipher):
    return [c % 256 for c in cipher]

# ===== Program Utama =====
# Input plaintext
message = input("Masukkan pesan (plaintext): ")

# Input rentang bilangan prima
start = int(input("Masukkan batas awal bilangan prima: "))
end = int(input("Masukkan batas akhir bilangan prima: "))

prime_list = primes_in_range(start, end)
print("Bilangan prima dalam rentang:", prime_list)

# Pilih p dan q dari daftar bilangan prima
p = int(input("Pilih bilangan prima p dari daftar di atas: "))
q = int(input("Pilih bilangan prima q dari daftar di atas (berbeda dengan p): "))
while q == p:
    q = int(input("q harus berbeda dari p. Masukkan q yang lain: "))

# Generate kunci
public, private = generate_keys(p, q)
print("Kunci Publik:", public)
print("Kunci Privat:", private)

# Enkripsi dan dekripsi
cipher = encrypt(message, public)
cipher_ascii = cipher_ascii_codes(cipher)
decrypted = decrypt(cipher, private)

print("Cipher (numerik):", cipher)
print("Cipher (kode ASCII):", cipher_ascii)
print("Pesan terdekripsi:", decrypted)