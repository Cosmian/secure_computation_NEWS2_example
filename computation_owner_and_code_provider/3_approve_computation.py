from cosmian_secure_computation_client import ComputationOwnerAPI, CodeProviderAPI
import os
import helpers
import time

cosmian_token = os.environ.get('COSMIAN_TOKEN')
computation_owner = ComputationOwnerAPI(cosmian_token)
code_provider = CodeProviderAPI(cosmian_token)

computation_uuid = input("Computation UUID: ")

while True:
    computation = computation_owner.get_computation(computation_uuid)
    if computation.enclave.identity is None:
        print("Waiting 5s the generation of the enclave identity…")
        time.sleep(5)
    else:
        break




### Check the computation

manifest = computation.enclave.identity.manifest
quote = computation.enclave.identity.quote

print("\n\n")
print(computation_owner.remote_attestation(quote))
print("\n\n")




### Computation Owner approves the computation
computation_owner.approve_participants(computation.uuid, "My super secure signature")




### Code Provider approves the computation

from cosmian_secure_computation_client.crypto.helper import seal
code_provider_symetric_key = helpers.read_bytes_from_file("/tmp/code_provider_symetric_key")
code_provider_sealed_symmetric_key = seal(code_provider_symetric_key, computation.enclave.identity.public_key)

code_provider.key_provisioning(computation.uuid, code_provider_sealed_symmetric_key)

