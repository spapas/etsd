etsd - Electronic Transmission of Sensitive Data
================================================

*Work in progress*


Transmit sensitive data throughout your organization using PGP (with the help of the openpgp.js library)

# Rationale

Some organizations need to transmit sensitive data between their departments/users. Such data may be personal details, 
work evaluation or even medical conditions. It is
Iimportant for such data to be delivered and be
seen only by its recipient and not by anybody
else.

One true and tested way for such data transmission
is to use GPG. The data will be encrypted with
the recipient's public key and only the recipient,
using his private key will be able to decrypt and
read it.

PGP is an old protocol that works fine with email
and even after all these years if it considered
by security experts as extremely secure. However
it is heavily criticized because it is difficult
to use properly leading to security breaches
due to usage errors.

This web application wants to build on PGP's
security but also offers a simple enough
work flow to minimize errors and security
breaches even for less security aware users.

# How it works
