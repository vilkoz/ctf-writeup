#!/usr/bin/python2

import sys
import random

key = sys.argv[1]
flag = '**CENSORED**'
flag = 'TWCTF{**CENSORED_FLAG**}'

assert len(key) == 13
assert max([ord(char) for char in key]) < 128
assert max([ord(char) for char in flag]) < 128

message = flag + "|" + key

random.seed(1)
encrypted = chr(random.randint(0, 128))

for i in range(0, len(message)):
  print 'enc:, encrypted', (encrypted, (encrypted[i]))
  encrypted += chr(
            (ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128
          )

print(encrypted.encode('hex'))
