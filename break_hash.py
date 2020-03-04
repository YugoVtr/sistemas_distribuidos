import argparse, hashlib
from lib.decorators import coroutine

def producer(file, next_coroutine):
    try:
        for line in file:
            next_coroutine.send(line)
    except ValueError as error:
        print(error)
    finally:
        next_coroutine.close()

@coroutine
def hasher(hexdigest, f_hash, next_coroutine):
    try:
        while True:
            plain_text = yield
            hashed = f_hash(plain_text.strip().encode("utf-8")).hexdigest()
            if hashed == hexdigest:
                next_coroutine.send(plain_text)
    except GeneratorExit:
        pass

@coroutine
def io_key_word():
    try:
        while True:
            key_word = yield
            print(key_word)
    except GeneratorExit:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hash", type=str)
    parser.add_argument("infile", type=argparse.FileType("r"))
    args = parser.parse_args()

    output = io_key_word()
    check_hash = hasher(args.hash, hashlib.md5, output)

    producer(args.infile, check_hash)

