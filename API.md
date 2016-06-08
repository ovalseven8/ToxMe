# API
For communication with the server, POST the following HTTPS requests (JSON) to
`https://example.tld/api`. For some actions you will need the server's public
key which can be found at `https://example.tld/pk`.

## Lookup:
Get the Tox ID of a user with the `lookup`-action:
```javascript
{ "action": 1,
  "name": "Username"       // Please only the username, not "Username@domain.tld"
}
```

#### Success:
In case the request was valid, you get the following response:

```javascript
{ "success_action_1": "Lookup has been successful.",
  "id": "49D7121A70E9723929649D1C3750A38B83C401705D632A8850A8973213093A6E"
}
```

#### Possible errors:
In case the request was invalid, you can get one of the following errors:
```javascript
// Username does not exist on the server:
{ "error_1": "This username is not registered." }
// The request was invalid because of several reasons (e.g. corrupt request):
{ "error_9": "Invalid request." }
// Error on the server's side:
{ "error_10": "Intern error." }
```

## Reverse lookup:
Get the username of a certain public key with the `reverse lookup`-action:
```javascript
{ "action": 2,
  "pk": "Public key"       // Public key (64 chars)
}
```

#### Success:
In case the request was valid, you get the following response:
```javascript
{ "success_action_2": "Reverse lookup has been successful.",
  "name": "Username"
}
```

#### Possible errors:
In case the request was invalid, you can get one of the following errors:
```javascript
// Public key is not registered on the server:
{ "error_2": "This public key is not registered." }
// The request was invalid because of several reasons (e.g. corrupt request):
{ "error_9": "Invalid request." }
// Error on the server's side:
{ "error_10": "Intern error." }
```

## Registration:
Register a certain public key with the `register`-action:
```javascript
{ "action": 3,
  "pk": "Public key"         // Public key (64 chars)
  "nonce": "Nonce"           // Random 24 byte nonce (Base64 encoded)
  "encrypted":               // Encrypted (Base64 encoded)
	{ "tox_id": "Tox ID"     // Full Tox ID (76 chars)
	  "name": "Username"     // Length: 1 - 60 chars
	  }
}
```
`"encrypted"` is encrypted using the server's public key, the secret key of the
user and the nonce (NaCl library).

#### Success:
In case the request was valid, you get the following response:
```javascript
{ "success_action_3": "The username has been registered." }
```

#### Possible errors:
In case the request was invalid, you can get one of the following errors:
```javascript
// The username that should be registered is too long
{ "error_3": "The username must be between 1 and 60 characters long." }
// The username that should be registered is already used on the server:
{ "error_4": "This username is already used." }
// Public key is already registered on the server. Only one registration is possible:
{ "error_5": "This public key is already registered." }
// The request was invalid because of several reasons (e.g. corrupt request):
{ "error_9": "Invalid request." }
// Error on the server's side:
{ "error_10": "Intern error." }
```

## Update:
Update the Tox ID (NoSpam value and checksum) of a certain username with the `update`-action:
```javascript
{ "action": 4,
  "pk": "Public key"         // Public key (64 chars)
  "nonce": "Nonce"           // Random 24 byte nonce (Base64 encoded)
  "encrypted": "Tox ID"      // Encrypted Tox ID (Base64 encoded)
}
```
`"encrypted"` is encrypted using the server's public key, the secret key of the
user and the nonce (NaCl library).

#### Success:
In case the request was valid, you get the following response:
```javascript
{ "success_action_4": "The username has been updated." }
```

#### Possible errors:
In case the request was invalid, you can get one of the following errors:
```javascript
// The public key of the Tox ID that should be updated is not registered on the server:
{ "error_6": "The public key is not registered. Nothing to update." }
// NoSpam value and so the checksum didn't change:
{ "error_7": "NoSpam value didn't change. Nothing to update" }
// The request was invalid because of several reasons (e.g. corrupt request):
{ "error_9": "Invalid request." }
// Error on the server's side:
{ "error_10": "Intern error." }
```

## Deletion:
Delete a certain username on the server with the `delete`-action:
```javascript
{ "action": 5,
  "pk": "Public key"         // Public key (64 chars)
  "nonce": "Nonce"           // Random 24 byte nonce (Base64 encoded)
  "encrypted": "Public key"  // Encrypted public key (Base64 encoded)
}
```
`"encrypted"` is encrypted using the server's public key, the secret key of the
user and the nonce (NaCl library).

#### Success:
In case the request was valid, you get the following response:
```javascript
{ "success_action_5": "The username has been deleted." }
```

#### Possible errors:
In case the request was invalid, you can get one of the following errors:
```javascript
// The public key that should be deleted on the server is not registered:
{ "error_8": "Public key is not registered. Nothing to delete." }
// The request was invalid because of several reasons (e.g. corrupt request):
{ "error_9": "Invalid request." }
// Error on the server's side:
{ "error_10": "Intern error." }
```
