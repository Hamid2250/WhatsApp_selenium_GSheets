def process_message(message, user):
    ##### English Response #####
    message = message.lower()
    print(f"reply {message}")
    if message in ("hi"):
        return 'Hello'
