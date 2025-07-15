from bids_validator import BIDSValidator

validator = BIDSValidator()
is_valid = validator.is_bids("/home/INT/idrissou.f/Bureau/Test")

print(f"Is valid BIDS dataset: {is_valid}")
