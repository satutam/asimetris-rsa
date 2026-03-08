# RSA Kriptografi - Implementasi Aritmatika Murni

Repositori ini berisi implementasi **RSA** menggunakan **aritmatika murni**, tanpa library eksternal.  
Menggunakan **Extended Euclidean Algorithm** untuk menghitung invers modular dan **modular exponentiation** untuk enkripsi/dekripsi.  

RSA didasarkan pada teori bilangan:

- Pilih dua bilangan prima `p` dan `q`.  
- Hitung:
```text
n = p * q
φ(n) = (p-1)*(q-1)
````

* Pilih `e` sehingga `1 < e < φ(n)` dan `gcd(e, φ(n)) = 1`.
* Hitung `d` sebagai invers modular dari `e modulo φ(n)`:

```text
d * e ≡ 1 mod φ(n)
```

* Kunci publik: `(e, n)`
* Kunci privat: `(d, n)`

Rumus enkripsi dan dekripsi:

```text
c ≡ m^e mod n
m ≡ c^d mod n
```

---

## Usage

Fungsi-fungsi utama:

* `generate_keys(p, q)` → Membuat kunci publik dan privat
* `encrypt(message, public)` → Enkripsi pesan
* `decrypt(cipher, private)` → Dekripsi pesan
* `cipher_ascii_codes(cipher)` → Representasi ciphertext sebagai kode ASCII

Contoh alur penggunaan:

```python
from generate_keys import generate_keys
from encrypt import encrypt
from decrypt import decrypt
from cipher_ascii_codes import cipher_ascii_codes

p = 61
q = 53
public, private = generate_keys(p, q)

message = "HELLO"
cipher = encrypt(message, public)
cipher_ascii = cipher_ascii_codes(cipher)
decrypted = decrypt(cipher, private)

print("Cipher numerik:", cipher)
print("Cipher ASCII:", cipher_ascii)
print("Pesan terdekripsi:", decrypted)
```

---

## Contoh Pembuatan Kunci

### Langkah 1: Pilih bilangan prima

```python
p = 61
q = 53
```

### Langkah 2: Hitung n dan φ(n)

```python
n = 3233
φ(n) = 3120
```

### Langkah 3: Pilih e (coprime dengan φ(n))

```python
e = 17
```

Gunakan **Extended Euclidean Algorithm** untuk mengecek:

```text
3120 = 17*183 + 9
17   = 9*1 + 8
9    = 8*1 + 1
8    = 1*8 + 0
gcd(17, 3120) = 1 → e valid
```

### Langkah 4: Hitung d

```text
d * e ≡ 1 mod φ(n)
Hasil EEA:
-367*17 + 2*3120 = 1
d = -367 mod 3120 = 2753
```

**Hasil Kunci:**

```text
Kunci Publik : (17, 3233)
Kunci Privat: (2753, 3233)
```

---

## Contoh Enkripsi

Enkripsi huruf `H` (ASCII 72):

```python
c = 72^17 mod 3233 = 3000
```

Langkah **modular exponentiation**:

| Pangkat | Perhitungan      | Hasil mod 3233 |
| ------- | ---------------- | -------------- |
| 1       | 72               | 72             |
| 2       | 72^2 = 5184      | 1951           |
| 4       | 1951^2 = 3804001 | 2790           |
| 8       | 2790^2 = 7784100 | 367            |
| 16      | 367^2 = 134689   | 2134           |
| 17      | 2134*72          | 3000           |

Ciphertext numerik: `[3000, ...]`

### Representasi ASCII Cipher

```python
cipher_ascii = [c % 256 for c in cipher]
```

Contoh:

```python
cipher = [3000, 2183]
cipher_ascii = [184, 135]
```

> Nilai ini menunjukkan **kode ASCII dari setiap byte ciphertext** (tidak selalu karakter printable).

---

## Contoh Dekripsi

Dekripsi `c = 3000` dengan `d = 2753`:

```python
m = 3000^2753 mod 3233 = 72
ASCII 72 → H
```

Pesan asli berhasil dipulihkan.

---

## Extended Euclidean Algorithm

Fungsi EEA digunakan untuk mencari **invers modular**:

```python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y
```

---

## Modular Exponentiation

Digunakan untuk **menghitung m^e mod n** atau **c^d mod n** secara efisien:

```python
def modexp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result
```

---

## Guidelines for contribution

* Fork repository ini
* Buat PR untuk perbaikan atau fitur baru
* Pastikan semua perubahan diuji secara lokal
