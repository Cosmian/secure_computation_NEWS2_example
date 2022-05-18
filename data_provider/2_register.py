from cosmian_secure_computation_client import DataProviderAPI
import os
import helpers

cosmian_token = os.environ.get('COSMIAN_TOKEN')
data_provider = DataProviderAPI(cosmian_token)

computation_uuid = input("Computation UUID: ")

data_provider_public_key = helpers.generate_pgp_key("some_data_provider_email@example.org")

computation = data_provider.register(computation_uuid, data_provider_public_key)
