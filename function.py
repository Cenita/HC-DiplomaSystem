import hashlib

if __name__ == '__main__':
    print(hashlib.md5("asfasfasf".encode('utf-8')).hexdigest())