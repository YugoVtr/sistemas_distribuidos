if [ ! -f files/rockyou.txt ]; then
    tar -xf files/rockyou.tar.gz -C files
fi

# Create the hash SHA-1 from file example.txt and try to break it
echo "\n======= START WITH COROUTINES ======="
time python break_hash.py $(sha1sum -t files/example.txt | awk '{ print $1 }') files/rockyou.txt
echo "\n======= START WITHOUT COROUTINES ======="
time python main.py $(sha1sum -t files/example.txt | awk '{ print $1 }') files/rockyou.txt

rm files/rockyou.txt
