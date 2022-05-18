import random
import string

def generate_pgp_key(email):
    letters = string.ascii_lowercase
    random_suffix = ''.join(random.choice(letters) for i in range(10))

    email = email.replace("@", f"+{random_suffix}@")

    import subprocess
    subprocess.Popen(['gpg', '--batch', '--passphrase', '', '--quick-generate-key', email, 'ed25519', 'cert', 'never'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, universal_newlines=True).communicate()
    public_key, stderr = subprocess.Popen(['gpg', '--export', '--armor', email], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, universal_newlines=True).communicate()

    return public_key


def save_bytes_to_file(path, bytes):
    f = open(path, "wb")
    f.write(bytes)
    f.close()

def read_bytes_from_file(path):
    f = open(path, "rb")
    return f.read()
