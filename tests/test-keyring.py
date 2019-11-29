import keyring

strategy = 'dexbot-arb-cointiger'

keyring.get_keyring()

keyring.set_password(strategy, "apikey", "#$PUPIO$OIJDSFDF")
keyring.set_password(strategy, "secret", "welrkjap3o54598345aa0FDF")

apikey = keyring.get_password(strategy, "apikey")
print(f'{strategy} apikey: {apikey}')

cred = keyring.get_credential(strategy, 'apikey')
print(f'credential: {cred}')
