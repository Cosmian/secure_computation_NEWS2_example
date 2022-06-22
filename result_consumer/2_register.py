from pathlib import Path
from cosmian_secure_computation_client import ResultConsumerAPI
from cosmian_secure_computation_client.crypto.context import CryptoContext
import os

cosmian_token = os.environ.get('COSMIAN_TOKEN')
words = Path("/tmp/words").read_text()
result_consumer = ResultConsumerAPI(cosmian_token, CryptoContext(words=words))

computation_uuid = input("Computation UUID: ")

computation = result_consumer.register(computation_uuid)




### Save keys for later

Path("/tmp/result_consumer_asymmetric_keys_seed").write_bytes(result_consumer.ctx.ed25519_seed)
Path("/tmp/result_consumer_symmetric_key").write_bytes(result_consumer.ctx.symkey)