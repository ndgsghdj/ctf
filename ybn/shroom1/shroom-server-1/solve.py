import pickletools
import base64

pickled = base64.b64decode("gASVPQAAAAAAAACMCF9fbWFpbl9flIwJU2F2ZVN0YXRllJOUKYGUfZQojARuYW1llIwGbmlrb2xhlIwGZmFybWVklEsBdWIu".encode("utf-8"))
pickletools.dis(pickled)
