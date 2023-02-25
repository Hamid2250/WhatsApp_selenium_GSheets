def process_message(message, user):
    ##### English Response #####
    # message = message.lower()
    reply = []
    for msg in message:
    
        if msg in ("هلا"):
            reply.append('هلا')
        elif msg.lower() in ("hi"):
            reply.append('Hey!')
        # else:
        #     return 'ERROR'
    print('\n'.join(reply))
    return '\n'.join(reply)