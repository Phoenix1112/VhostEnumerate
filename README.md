# VhostEnumerate
Virtual Host Enumerate


# installation instructions

```
git clone https://github.com/Phoenix1112/VhostEnumerate.git

cd VhostEnumerate

pip3 install -r requirements.txt
```

# Usage

```

python3 VhostEnumerate.py -u https://example.com

python3 VhostEnumerate.py -u https://example.com -t 30

python3 VhostEnumerate.py  -l /path/urllist.txt -w /path/other_wordlist.txt

cat urllist.txt | python3 VhostEnumerate.py -s -o output.txt

```

# Note = Pipe method will not work if you are using windows. You can run program on windows using the -l or -u parameters. If you are using linux, you can use the program as you wish.
