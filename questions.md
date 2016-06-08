# Questions

##### Why isn't it possible to register a username via a web interface?
While other ToxMe services provide the option to register a username via a nice
web interface, this is not possible here. There are different reasons for that 
decision:
 - It should only for the owner of the public key be possible to register, 
 update or delete his account on the server
 - A well-designed integration of ToxMe in Tox clients like qTox makes it much
 more comfortable to handle the registration etc. For example it's possible when
 you change your NoSpam value that the client will automatically send an
 `update` request to the ToxMe service you are registered on
 - The goal was to create a preferably lightweight ToxMe service

##### Can someone else register, delete or update my account?
No. Only the owner of the public key - thanks to cryptography - can do that.

##### How does ToxMe prevent replay attacks?
A well-configured ToxMe service should only be accessible via a strong TLS
connection. Because of that replay attacks are not possible. Additionally,
when you never used the `update` or `delete` action there is also in theory
no chance for a replay attack.

##### But is not TLS broken?
There are definitely some issues with TLS but a well-configured service that is
only accessible via a strong TLS connection should be relatively secure.
Moreover, ToxMe also uses NaCl for the `register`, `update` and `delete` actions.

##### So is ToxMe secure or not?
Unfortunately, it is not possible to answer this question with a simple "Yes"
or "No". First of all, it is important to understand that the most secure way
will always be to validate and use only Tox IDs. That's especially the case
when someone uses Tox for pretty sensitive communication (what should not be
the case at the moment because Tox is still alpha-software).

So let's be honest: You can use ToxMe services definitely without the need to
be afraid and it's actually much more comfortable to add an user like
`alice@domain.tld` than a 76 hexadecimal Tox ID. You just should know that
there will never be 100% security when you use the internet and that you should
only register on ToxMe services you trust. And when you use Tox for sensitive
communication, check and validate the Tox ID of the person you want to
communicate with. For the rest: Happy toxing!
