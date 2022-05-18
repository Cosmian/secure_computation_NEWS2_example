from cosmian_secure_computation_client import DataProviderAPI
import os
import json

cosmian_token = os.environ.get('COSMIAN_TOKEN')
data_provider = DataProviderAPI(cosmian_token)

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

from cosmian_secure_computation_client.crypto.helper import random_symkey
data_provider_symmetric_key = random_symkey()

data_provider.push_data(computation_uuid, data_provider_symmetric_key, "responses.json", bytes(data_as_json_string, "utf-8"))
data_provider.done(computation_uuid)




### Data Provider approves the computation

from cosmian_secure_computation_client.crypto.helper import seal
data_provider_sealed_symetric_key = seal(data_provider_symmetric_key, computation.enclave.identity.public_key)

data_provider.key_provisioning(computation_uuid, data_provider_sealed_symetric_key)
