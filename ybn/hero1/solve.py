from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from sympy import factorint

# Given values
g = 1083266756892566929704202779668530503918356339884480137428763337699212285036809493492769953109699
n = 910055459205441397806360422016777495662828495067966263959779494321033765620236211205464484648836676708321335826462446127392412934291317355596317016931689033058925189216085451787227624642272788029282490814869716133218114603793823573
ct = 74973089851474944376922930978693557571357882598872160120708819257500976611064553844164888105895794299800012768062473173491537193811809441418095392309337015930057229010145801066989029453675221378137220150175359745521751136851772713740557492526421814107620635351965061601872717995811784506117421829558676362255

# Step 1: Factorize g = q * e to extract q and e
def factor_g(g):
    factors = factorint(g)
    if len(factors) == 2:  # Ensure g has exactly two prime factors
        q, e = list(factors.keys())
        return q, e
    else:
        raise ValueError("g does not have exactly two prime factors")

q, e = factor_g(g)
print(f"q = {q}, e = {e}")

# Step 2: Exploit a input vulnerability (e.g., set a to a simple value like 1)
a = 1  # We use a = 1 for simplicity
b = 0  # b = 0 (can try other values as well)

# Now, compute n with the chosen 'a'
n = 1 * q * e * 1234567890  # We simplify the computation of n

# Step 3: Factorize n to get p, q, and y
def factor_n(n, q):
    n_wo_q = n // q
    factors = factorint(n_wo_q)
    
    if len(factors) == 2:  # Assuming n_wo_q is a product of p and y
        p, y = list(factors.keys())
        return p, y
    else:
        raise ValueError("Unable to factor n into p and y")

p, y = factor_n(n, q)
print(f"p = {p}, y = {y}")

# Step 4: Compute enc from ct and y
def compute_enc(ct, y):
    return ct // y

enc = compute_enc(ct, y)
print(f"enc = {enc}")

# Step 5: Find modular inverse of e modulo (p-1)*(q-1) to get d
def mod_inverse(e, phi_n):
    return pow(e, -1, phi_n)

phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
print(f"d = {d}")

# Step 6: Decrypt the flag by computing pow(enc, d, n)
def decrypt_flag(enc, d, n):
    flag_long = pow(enc, d, n)
    return long_to_bytes(flag_long)

flag = decrypt_flag(enc, d, n)
print(f"Flag: {flag.decode()}")

