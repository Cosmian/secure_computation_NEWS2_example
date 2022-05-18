from cosmian_secure_computation_client import ResultConsumerAPI
import os
import time

cosmian_token = os.environ.get('COSMIAN_TOKEN')
result_consumer = ResultConsumerAPI(cosmian_token)

computation_uuid = input("Computation UUID: ")
computation = result_consumer.get_computation(computation_uuid)





### Result Consumer checks the computation

manifest = computation.enclave.identity.manifest
quote = computation.enclave.identity.quote

print("\n\n")
print(result_consumer.remote_attestation(quote))
print("\n\n")





### Result Consumer approves the computation

from cosmian_secure_computation_client.crypto.helper import random_symkey
result_consumer_symmetric_key = random_symkey()

from cosmian_secure_computation_client.crypto.helper import seal
result_consumer_sealed_symetric_key = seal(result_consumer_symmetric_key, computation.enclave.identity.public_key)

result_consumer.key_provisioning(computation_uuid, result_consumer_sealed_symetric_key)





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

from cosmian_secure_computation_client.crypto.helper import decrypt
results = decrypt(encrypted_results, result_consumer_symmetric_key)

print(int(results.decode("utf-8")))
