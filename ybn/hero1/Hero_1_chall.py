from Crypto.Util.number import getPrime, bytes_to_long

flag = b"YBN24{????????????????????????}"

p = getPrime(256)
q = getPrime(256)
y = getPrime(256)
e = getPrime(64)
c = getPrime(32)


try:
    a = int(eval(input("a: ")))
    b = int(eval(input("b: ")))

    assert a > 0
except:
    quit()


g = q * e
n = ((a) ** (b + c)) * p * q * y

enc = pow(bytes_to_long(flag), e, n)

ct = enc * y

print("g = {}".format(g))
print("n = {}".format(n))
print("ct = {}".format(ct))


