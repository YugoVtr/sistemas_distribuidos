import argparse, hashlib

def hasher(hexdigest, f_hash, wordlist):
    try:
        for plain_text in wordlist:
            hashed = f_hash(plain_text.strip()).hexdigest()
            if hashed == hexdigest:
                output = "passphrase is: %s" % plain_text.decode('utf-8')
                print(output)
                return
        print("passphrase not found")
    except ValueError as e:
        print(e)   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hash", type=str)
    parser.add_argument("infile", type=argparse.FileType("rb"))
    args = parser.parse_args()

    hasher(args.hash, hashlib.sha1, args.infile)

