# Kryptobits
#### A hybrid encryption system to encrypt any message using symmetric(AES-256) and asymmetric(RSA-4K) algorithms

## API's to encrypt and decrypt the messages using RSA-4K algorithm
### /krs/v1/pubkey
 - API to get public key and respective key_id from the store. 
 - Public Key can be retrieved by anyone.

### /krs/v1/pvtkey
 - User authenticates and provides the key_id as Input to the API.
 - Respective Private Key will be given by the API
