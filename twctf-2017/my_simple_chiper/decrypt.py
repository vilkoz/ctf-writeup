def decrypt(key, message):
    decrypted = ''
    for i in range(len(message) -1, 0, -1):
        decrypted += chr(
                (ord(message[ i ]) -
                ord(key[ (i-1) % len(key) ]) -
                ord(message[ i - 1 ])) % 128)
    return decrypted[::-1]

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

def main():
    with open('encrypted.txt', 'r') as f:
        encrypted = f.read().replace('\n', '').decode('hex')
    print list(encrypted)
    new_key = ['A'] * 13
    for i in range(0, len(new_key)):
        try:
            new_key[i] = bruteKeyChar(i, encrypted, new_key)[0]
            print 'char: %2c %5d key_num: %d' % (new_key[i], ord(new_key[i]), i % len(new_key))
        except Exception:
            print 'not found char ', i
    print decrypt(''.join(new_key), encrypted)

if __name__ == "__main__":
    main()
