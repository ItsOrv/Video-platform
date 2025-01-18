import uuid

def process_payment(user, amount):
    transaction_id = str(uuid.uuid4())
    # Logic to integrate with payment gateway
    success = True  # Assume payment succeeds
    return transaction_id, success
