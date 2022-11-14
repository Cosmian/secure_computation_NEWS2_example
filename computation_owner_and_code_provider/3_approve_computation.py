from pathlib import Path
from cosmian_secure_computation_client import CodeProviderAPI
from cosmian_secure_computation_client.crypto.context import CryptoContext
from cosmian_secure_computation_client.api.computations import EnclaveIdentityLockError
import os
import time

cosmian_token = os.environ.get('COSMIAN_TOKEN')




### Read keys from files from first step

words = Path("/tmp/words").read_text()
code_provider_asymmetric_keys_seed = Path("/tmp/code_provider_asymmetric_keys_seed").read_bytes()
code_provider_symmetric_key = Path("/tmp/code_provider_symmetric_key").read_bytes()

code_provider = CodeProviderAPI(cosmian_token, CryptoContext(
    words = words,
    ed25519_seed = code_provider_asymmetric_keys_seed,
    symkey = code_provider_symmetric_key,
))

computation_uuid = input("Computation UUID: ")

while True:
    computation = code_provider.get_computation(computation_uuid)

    if computation.enclave.identity is None:
        print("Waiting 5s the generation of the enclave identity…")
        time.sleep(5)
    elif isinstance(computation.enclave.identity, EnclaveIdentityLockError):
        raise Exception(f"The enclave cannot lock its identity because there is an error in the entrypoint.\n\n{computation.enclave.identity.stdout}\n\n{computation.enclave.identity.stderr}")
    else:
        break




### Check the computation

manifest = computation.enclave.identity.manifest
quote = computation.enclave.identity.quote

print("\n\n")
print(code_provider.remote_attestation(quote))
print("\n\n")




### Code Provider approves the computation

code_provider.key_provisioning(computation.uuid, computation.enclave.identity.public_key)

