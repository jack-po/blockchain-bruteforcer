#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
import base64, time, urllib2, json, sys
import argparse
from permutations import capitalize, add_symbols


parser = argparse.ArgumentParser("Blockchain password recovery tool")
parser.add_argument("login", help="login at blockchain.info")
parser.add_argument("--dictionary", "-d", help="path to dictionary file", default="dictionary.txt")
parser.add_argument("--num", "-n", help="print every 'n' password", type=int, default=10)
args = parser.parse_args()


class AESCipher:
    BLOCKSIZE = 4

    def __init__( self, rawdata ):
        data = base64.b64decode(rawdata)
        self.data = data
        self.iv = data[:self.BLOCKSIZE*4]

    def unpad(self, data):
        pad = ord(data[-1:])
        maxPad = self.BLOCKSIZE * 4

        if pad > maxPad:
            raise Exception("Invalid padding length")

        return data[maxPad:-pad]

    def decrypt( self, password, iterations = 10 ):
        key = PBKDF2(password, self.iv, iterations).read(32)

        cipher = AES.new(key, AES.MODE_CBC, self.iv)
        return self.unpad(cipher.decrypt(self.data))


class Dictionary:
    def __init__(self, path):
        self.dict_file = open(path)

    @capitalize
    @add_symbols
    def __iter__(self):
        return self

    def next(self):
        return self.dict_file.next().strip("\n")


if __name__ == "__main__":
    print "Login: %s" % args.login
    print "Dictionary: %s" % args.dictionary

    response = urllib2.urlopen("https://blockchain.info/wallet/%s?format=json&resend_code=false&ct=%d" % (
        args.login,
        int(round(time.time() * 1000))
    ))

    json_data = json.loads(response.read())

    try:
        json_data = json.loads(json_data["payload"])
    except:
        pass

    iterations = int(json_data["pbkdf2_iterations"]) if "pbkdf2_iterations" in json_data else 10

    print "Iterations per password: %d" % iterations
    

    aes = AESCipher(json_data["payload"])
    dictionary = iter(Dictionary(args.dictionary))

    i = 0
    try:
        while True:
            password = next(dictionary)

            i += 1
            if i >= args.num:
                print password
                i = 0

            try:
                decrypted =  aes.decrypt(password, iterations)
                json_result = json.loads(decrypted)

                ## Password finded! ##
                print decrypted
                print 'Your password is:"%s"' % password
                break

            except Exception:
                pass

    except StopIteration:
        pass
    finally:
        del dictionary

    raw_input("Press Enter to exit...")