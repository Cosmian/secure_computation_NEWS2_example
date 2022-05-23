# Secure Computation: National Early Warning Score

Compute the [National Early Warning Score](https://www.mdcalc.com/national-early-warning-score-news-2) in a [Cosmian Secure Computation](https://docs.cosmian.com/secure_computation/).

There are 3 participants in this computation:
- 🏢 the Computation Owner and Code Provider (the company with the private algorithm; for this example, it is the public National Early Warning Score algorithm)
- 🤒 the Data Provider (the patient who sends his medical information encrypted)
- 👩‍⚕️ the Result Consumer (the doctor who receives the final score and acts accordingly)

[Cosmian Secure Computation](https://docs.cosmian.com/secure_computation/) guarantees that:
- neither 🌌 Cosmian nor the ☁️ cloud provider can see the private company algorithm, the patient medical information, or the final score
- 🏢 the private company cannot access the patient medical information, nor the patient final score
- 👩‍⚕️ the doctor cannot access the complete medical information (only the final score), nor the private company algorithm
- 🤒 the patient cannot access the private company algorithm, nor his final score (this can be changed by allowing the patient to be on the result consumers list)

|                        | Algorithm | Full Medical Information | Final Medical Score |
|------------------------|----------|---------------------------|---------------------|
| 🌌 Cosmian                | 🚫        | 🚫                         | 🚫                   |
| ☁️ Cloud Provider (Azure) | 🚫        | 🚫                         | 🚫                   |
| 🏢 Private Company        | ✅        | 🚫                         | 🚫                   |
| 🤒 Patient                | 🚫        | ✅                         | 🚫                   |
| 👩‍⚕️ Doctor                 | 🚫        | 🚫                        | ✅                   |

## Installation

```bash
pip install cosmian_secure_computation_client
```

## Usage

Each participant needs a Cosmian token store in `COSMIAN_TOKEN` environment variable. Request your token for free on [https://console.cosmian.com/](https://console.cosmian.com/)

1. 🏢 Run `computation_owner_and_code_provider/1_create_computation.py` (ask the 3 participants' emails, generate key pair, and sends the encrypted code)
1. 🤒 Run `data_provider/2_register.py` (generate key pair and join the computation)
1. 👩‍⚕️ Run `result_consumer/2_register.py` (generate key pair and join the computation)
1. 🏢 Run `computation_owner_and_code_provider/3_approve_computation.py` (sends the encrypted symmetric key)
1. 🤒 Run `data_provider/3_send_data.py` (respond to questions, send encrypted responses, and send the encrypted symmetric key)
1. 👩‍⚕️ Run `result_consumer/4_get_results.py` (send encrypted symmetric key, wait for the result, and decrypt the final score)
