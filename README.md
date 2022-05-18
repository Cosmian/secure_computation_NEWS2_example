# Secure Computation: National Early Warning Score

Compute the [National Early Warning Score](https://www.mdcalc.com/national-early-warning-score-news-2) in a Cosmian secure enclave.

## Installation

```bash
pip install cosmian_secure_computation_client
```

## Usage

1. Run `computation_owner_and_code_provider/1_create_computation.py`
1. Run `data_provider/2_register.py`
1. Run `result_consumer/2_register.py`
1. Run `computation_owner_and_code_provider/3_approve_computation.py`
1. Run `data_provider/3_send_data.py`
1. Run `result_consumer/4_get_results.py`
