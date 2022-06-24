from pathlib import Path
from cosmian_secure_computation_client import DataProviderAPI
from cosmian_secure_computation_client.crypto.context import CryptoContext
import os

cosmian_token = os.environ.get('COSMIAN_TOKEN')
words = Path("/tmp/words").read_text()
data_provider = DataProviderAPI(cosmian_token, CryptoContext(words=words))

computation_uuid = input("Computation UUID: ")

computation = data_provider.register(computation_uuid)




### Save keys for later

Path("/tmp/data_provider_asymmetric_keys_seed").write_bytes(data_provider.ctx.ed25519_seed)
Path("/tmp/data_provider_symmetric_key").write_bytes(data_provider.ctx.symkey)