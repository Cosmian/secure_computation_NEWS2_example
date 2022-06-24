from pathlib import Path
from cosmian_secure_computation_client import ResultConsumerAPI
from cosmian_secure_computation_client.crypto.context import CryptoContext
import os
import time

cosmian_token = os.environ.get('COSMIAN_TOKEN')




### Read keys from files from first step

words = Path("/tmp/words").read_text()
result_consumer_asymmetric_keys_seed = Path("/tmp/result_consumer_asymmetric_keys_seed").read_bytes()
result_consumer_symmetric_key = Path("/tmp/result_consumer_symmetric_key").read_bytes()

result_consumer = ResultConsumerAPI(cosmian_token, CryptoContext(
    words = words,
    ed25519_seed = result_consumer_asymmetric_keys_seed,
    symkey = result_consumer_symmetric_key,
))

computation_uuid = input("Computation UUID: ")
computation = result_consumer.get_computation(computation_uuid)





### Result Consumer checks the computation

manifest = computation.enclave.identity.manifest
quote = computation.enclave.identity.quote

print("\n\n")
print(result_consumer.remote_attestation(quote))
print("\n\n")





### Result Consumer approves the computation

result_consumer.key_provisioning(computation_uuid, computation.enclave.identity.public_key)





### Result Consumer waits the end of the computation

while True:
    computation = result_consumer.get_computation(computation_uuid)

    if len(computation.runs.previous) == 1:
        run = computation.runs.previous[0]

        if run.exit_code != 0:
            raise Exception(f"Run fail with stdout. {run.stdout}")
        else:
            break
    else:
        print("Waiting 5s end of computation…")
        time.sleep(5)





### Result Consumer decrypts the results

encrypted_results = result_consumer.fetch_results(computation_uuid)
results = result_consumer.ctx.decrypt(encrypted_results)

final_score = int(results.decode("utf-8"))

if final_score <= 2:
    final_score_as_string = "low risk"
elif final_score <= 4:
    final_score_as_string = "low-medium risk"
elif final_score <= 6:
    final_score_as_string = "medium risk"
else:
    final_score_as_string = "high risk"


print(f"Patient score is {final_score} ({final_score_as_string})")
