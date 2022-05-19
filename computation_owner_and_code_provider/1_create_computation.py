from cosmian_secure_computation_client import ComputationOwnerAPI, CodeProviderAPI
import helpers
import os
from pathlib import Path

cosmian_token = os.environ.get('COSMIAN_TOKEN')
my_email = input("My email: ")

computation_owner = ComputationOwnerAPI(cosmian_token)
code_provider = CodeProviderAPI(cosmian_token)




### Computation Owner creates the computation

owner_public_key = helpers.generate_pgp_key(my_email)

data_provider_email = input("Data Provider email: ")
result_consumer_email = input("Result Consumer email: ")

computation = computation_owner.create_computation(
    'National Early Warning Score (NEWS) 2',
    owner_public_key=owner_public_key,
    code_provider_email=my_email,
    data_providers_emails=[data_provider_email],
    result_consumers_emails=[result_consumer_email]
)

print(f"\n\nThe computation ID is {computation.uuid}\n")




### Code Providers registers inside the computation

code_provider_public_key = helpers.generate_pgp_key(my_email)
computation = code_provider.register(computation.uuid, code_provider_public_key)




### Code Providers sends code

from cosmian_secure_computation_client.crypto.helper import random_symkey
code_provider_symmetric_key = random_symkey()
helpers.save_bytes_to_file("/tmp/code_provider_symetric_key", code_provider_symmetric_key)

code_provider.upload(computation.uuid, code_provider_symmetric_key, Path(os.path.dirname(__file__)) / "code")