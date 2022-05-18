# Secure Computation: National Early Warning Score

Compute the [National Early Warning Score](https://www.mdcalc.com/national-early-warning-score-news-2) in a Cosmian secure enclave.

There is 3 participants in this computation:
- the computation owner and code provider (the startup with the private algorithm, for the example it's the public National Early Warning Score algorithm)
- the data provider (the patient who sends his medical information encrypted)
- the result consumer (the doctor who receives the final score and acts accordingly)

## Installation

```bash
pip install cosmian_secure_computation_client
```

## Usage

Each participant needs a Cosmian token store in `COSMIAN_TOKEN` environment variable. Request your token for free on [https://console.cosmian.com/](https://console.cosmian.com/)

1. Run `computation_owner_and_code_provider/1_create_computation.py` (ask the 3 participants' emails, generate key pair and sends the encrypted code)
1. Run `data_provider/2_register.py` (generate key pair and join the computation)
1. Run `result_consumer/2_register.py` (generate key pair and join the computation)
1. Run `computation_owner_and_code_provider/3_approve_computation.py` (sends encrypted symmetric key)
1. Run `data_provider/3_send_data.py` (respond to questions, send encrypted responses and send encrypted symmetric key)
1. Run `result_consumer/4_get_results.py` (send encrypted symmetric key, wait the result and decrypt the final score)
