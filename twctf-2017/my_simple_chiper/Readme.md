# My simple cipher #twctf-2017 warmup crypto

## Task

```
This my first cipher system. Can you break it?
```
Given cipher.py and encrypted.txt, you need to recover encrypted information.

## Solution

Content of cipher.py
```python
import sys
import random

key = sys.argv[1]
flag = '**CENSORED**'

assert len(key) == 13
assert max([ord(char) for char in key]) < 128
assert max([ord(char) for char in flag]) < 128

message = flag + "|" + key

random.seed(1)
encrypted = chr(random.randint(0, 128))

for i in range(0, len(message)):
  print 'enc:, encrypted', (encrypted, (encrypted[i]))
  encrypted += chr((ord(message[i]) +
                    ord(key[i % len(key)]) +
                    ord(encrypted[i])) % 128)

print(encrypted.encode('hex'))

```

From the source code we can see that key must be 13 characters long and it is contained at the end of ciphertext, also we know that the first 6 characters of flag will be `TWCTF{`. But at first we need a decrypt function, we can write it just reversing original cipher:

```python
def decrypt(key, message):
    decrypted = ''
    for i in range(len(message) -1, 0, -1):
        decrypted += chr(
                (ord(message[ i ]) -
                ord(key[ (i-1) % len(key) ]) -
                ord(message[ i - 1 ])) % 128)
    return decrypted[::-1]
```

Note shift by one char to left when accessing key values, it is done because of one extra random char at the beginning of ciphertext. Now, we can derive the formula for the first six key characters: `x = (msg[n+1] - msg[n] - 'TWCTF{'[n]) % 128`. Remaining characters of key can be bruteforced, asserting that key character must be same with corresponding character in decrypted message.

```python
def bruteKeyChar(num, message, key):
    key_num = num % len(key)
    if key_num in range(0, 6):
        x = (ord(message[num + 1]) -
                ord(message[num]) -
                ord('TWCTF{'[key_num])) % 128
        return chr(x), x
    for i in range(0, 128):
        key[key_num] = chr(i % 128)
        decrypted = decrypt("".join(key), message)
        if decrypted[len(decrypted) - len(key) + key_num] == key[key_num]:
            print decrypted, key
            return key[key_num], i
    raise Exception('Not found!')
```

So let's recover message:

```
$ python2 decrypt.py
['|', '\x15', ':', 'G', 'K', 'j', '-', '?', '}', '?', 's', '(', 'p', '>', 'l', '-', '$', ':', '\x08', '>', '.', 'w', '<', 'E', 'T', 'w', 'H', 'f', '|', '\x15', '\x11', '3', '?', 'O', 't', '^']
char:  E    69 key_num: 0
char:  N    78 key_num: 1
char:  J    74 key_num: 2
char:  0    48 key_num: 3
char:  Y    89 key_num: 4
char:  H    72 key_num: 5
is-funHNbYHOLIDAd) ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'A', 'A', 'A', 'A', 'A', 'A']
char:  O    79 key_num: 6
is-fun!}HNbYHOLIDAY) ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'L', 'A', 'A', 'A', 'A', 'A']
char:  L    76 key_num: 7
is-fun!}|HNbYHOLIDAY! ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'L', 'I', 'A', 'A', 'A', 'A']
char:  I    73 key_num: 8
is-fun!}|ENbYHOLIDAY! ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'L', 'I', 'D', 'A', 'A', 'A']
char:  D    68 key_num: 9
is-fun!}|ENbYHOLIDAY! ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'L', 'I', 'D', 'A', 'A', 'A']
char:  A    65 key_num: 10
is-fun!}|ENJYHOLIDAY! ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'L', 'I', 'D', 'A', 'Y', 'A']
char:  Y    89 key_num: 11
TWCTF{Crypto-is-fun!}|ENJ0YHOLIDAY! ['E', 'N', 'J', '0', 'Y', 'H', 'O', 'L', 'I', 'D', 'A', 'Y', '!']
char:  !    33 key_num: 12
TWCTF{Crypto-is-fun!}|ENJ0YHOLIDAY!

```

[decrypt.py source code](decrypt.py)
