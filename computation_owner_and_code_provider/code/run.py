from cosmian_lib_sgx import Enclave
import json

def main() -> int:
    """Entrypoint of your code."""
    with Enclave() as enclave:
        import national_early_warning_score

        # Fetch all files send by Data Provider #0 (there is only one data provider for this computation)
        files = enclave.read(0)

        # Fetch the first file sent (there is only one file send for this computation)
        file_as_bytes_io = next(files)

        file_as_bytes = file_as_bytes_io.read()

        # The data received is a BytesIO, convert them to bytes with .read(), then to string with .decode("utf-8")
        file_as_string = file_as_bytes.decode("utf-8") 

        # The data provider sent us a JSON file
        data = json.loads(file_as_string)

        # Our module take the values sent by the patient and returns us a score (an integer)
        score_as_int = national_early_warning_score.run(data)

        # The result must be sent in bytes, so convert the integer to bytes
        score_as_bytes: bytes = str(score_as_int).encode()

        # Write the result for the Result Consumer #0 (there is only one result consumer for this computation)
        enclave.write(score_as_bytes, 0)

    return 0


if __name__ == "__main__":
    main()
