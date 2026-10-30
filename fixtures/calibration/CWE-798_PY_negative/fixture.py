import hmac

def login(password, externally_supplied_expected_password):
    return hmac.compare_digest(password, externally_supplied_expected_password)
