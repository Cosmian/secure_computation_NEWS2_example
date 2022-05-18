from cosmian_secure_computation_client import ResultConsumerAPI
import os
import helpers

cosmian_token = os.environ.get('COSMIAN_TOKEN')
result_consumer = ResultConsumerAPI(cosmian_token)

computation_uuid = input("Computation UUID: ")

result_consumer_public_key = helpers.generate_pgp_key("some_result_consumer_email@example.org")

computation = result_consumer.register(computation_uuid, result_consumer_public_key)
