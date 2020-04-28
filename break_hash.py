import hashlib, sys
from lib.decorators import coroutine

def hasher(hexdigest, f_hash, word_list):
    try:
        test = test_hash(hexdigest, f_hash)
        password = next( word_list )
        while( password ):
            test.send( password.strip() )
            password = next( word_list )
    except StopIteration:
        pass
    finally:
        test.close()
        sys.exit(0)

@coroutine
def test_hash(test_pwd, f_hash):
    try:
        while True:
            password = (yield)
            hashed = f_hash(password).hexdigest()
            if test_pwd == hashed:
                print("password is %s" % password)
                sys.exit(0)
    except GeneratorExit:
        print("Password not found")

if __name__ == "__main__":
    f_hash = hashlib.sha1
    hash_text = f_hash(b"asdf234").hexdigest()
    word_list = open("files/rockyou.txt", 'rb')

    hasher(hash_text, hashlib.sha1, word_list)
    word_list.close()

