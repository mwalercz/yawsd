def clear_passwords_from_message(message):
    return dict(
        path=message['path'],
        body={
            key: value if key.lower() != 'password' else '***'
            for key, value in message.get('body', {}).items()
        } if message.get('body') is not None else None
    )
