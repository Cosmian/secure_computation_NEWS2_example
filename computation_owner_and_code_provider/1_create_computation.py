from cosmian_secure_computation_client import ComputationOwnerAPI, CodeProviderAPI
from cosmian_secure_computation_client.crypto.context import CryptoContext
import os
from pathlib import Path

cosmian_token = os.environ.get('COSMIAN_TOKEN')
my_email = input("My email: ")

computation_owner = ComputationOwnerAPI(cosmian_token)




### Computation Owner creates the computation

data_provider_email = input("Data Provider email: ")
result_consumer_email = input("Result Consumer email: ")

computation = computation_owner.create_computation(
    'National Early Warning Score (NEWS) 2',
    code_provider_email=my_email,
    data_providers_emails=[data_provider_email],
    result_consumers_emails=[result_consumer_email]
)

print(f"\n\nThe computation ID is {computation.uuid}\n")




### All participants must share the same secret

words = ComputationOwnerAPI.random_words()
Path("/tmp/words").write_text(f"{words[0]} {words[1]} {words[2]}")




### Code Providers registers inside the computation

code_provider = CodeProviderAPI(cosmian_token, CryptoContext(words=words))
computation = code_provider.register(computation.uuid)




### Code Providers sends code

code_provider.upload(computation.uuid, Path(os.path.dirname(__file__)) / "code")




### Save keys for later

Path("/tmp/code_provider_asymmetric_keys_seed").write_bytes(code_provider.ctx.ed25519_seed)
Path("/tmp/code_provider_symmetric_key").write_bytes(code_provider.ctx.symkey)