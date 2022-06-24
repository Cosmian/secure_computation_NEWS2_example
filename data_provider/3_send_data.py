from pathlib import Path
from cosmian_secure_computation_client import DataProviderAPI
from cosmian_secure_computation_client.crypto.context import CryptoContext
import os
import json

cosmian_token = os.environ.get('COSMIAN_TOKEN')




### Read keys from files from first step

words = Path("/tmp/words").read_text()
data_provider_asymmetric_keys_seed = Path("/tmp/data_provider_asymmetric_keys_seed").read_bytes()
data_provider_symmetric_key = Path("/tmp/data_provider_symmetric_key").read_bytes()

data_provider = DataProviderAPI(cosmian_token, CryptoContext(
    words = words,
    ed25519_seed = data_provider_asymmetric_keys_seed,
    symkey = data_provider_symmetric_key,
))

computation_uuid = input("Computation UUID: ")
computation = data_provider.get_computation(computation_uuid)





### Data Provider checks the computation

manifest = computation.enclave.identity.manifest
quote = computation.enclave.identity.quote

print("\n\n")
print(data_provider.remote_attestation(quote))
print("\n\n")





### Data Provider responds to questions

breaths_per_minute = int(input("Respiratory rate, breaths per minute: "))
hypercapnic_respiratory_failure = input("Hypercapnic respiratory failure (yes, no): ")
spo2 = int(input("SpO₂ (%): "))
room_air_or_supplemental_o2 = input("Room air or supplemental O₂ (room, supplemental): ")
temperature = float(input("Temperature: "))
systolic_bp_mmhg = int(input("Systolic BP, mmHg: "))
beats_by_minute = int(input("Pulse, beats per minute: "))
consciousness = input("Consciousness (yes, no): ")

data_as_json_string = json.dumps({
    'breaths_per_minute': breaths_per_minute,
    'hypercapnic_respiratory_failure': hypercapnic_respiratory_failure,
    'spo2': spo2,
    'room_air_or_supplemental_o2': room_air_or_supplemental_o2,
    'temperature': temperature,
    'systolic_bp_mmhg': systolic_bp_mmhg,
    'beats_by_minute': beats_by_minute,
    'consciousness': consciousness,
})



### Data Provider sends data

data_provider.push_data(computation_uuid, "responses.json", bytes(data_as_json_string, "utf-8"))
data_provider.done(computation_uuid)




### Data Provider approves the computation

data_provider.key_provisioning(computation_uuid, computation.enclave.identity.public_key)
