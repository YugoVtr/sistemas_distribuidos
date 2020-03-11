import argparse, hashlib
from lib.decorators import coroutine

def hasher(hexdigest, f_hash, readline, output):
    try:
        plain_text = next( readline )
        while plain_text:
            hashed = f_hash(plain_text.strip()).hexdigest()
            if hashed == hexdigest:
                output.send(plain_text)
                plain_text = None
            else:
                plain_text = next( readline )
    except StopIteration:
        output.send(None)
    finally:
        readline.close()
        output.close()   

@coroutine
def producer(wordlist):
    try:
        for line in wordlist:
            yield line
    except GeneratorExit as e:
        pass

@coroutine
def found_key_word():
    try:
        while True:
            key_word = yield
            if key_word:
                output = "passphrase is: %s" % key_word.decode('utf-8')
            else:
                output = "passphrase not found"    
            print(output)
    except GeneratorExit:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hash", type=str)
    parser.add_argument("infile", type=argparse.FileType("rb"))
    args = parser.parse_args()

    output = found_key_word()
    readline = producer(args.infile)

    hasher(args.hash, hashlib.sha1, readline, output)

