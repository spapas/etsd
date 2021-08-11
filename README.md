etsd - Electronic Transmission of Sensitive Data
================================================

*Work in progress*


Transmit sensitive data throughout your organization using PGP (with the help of the openpgp.js library)

# Rationale

Some organizations need to transmit sensitive data between their departments/users. Such data may be personal details, 
work evaluation or even medical conditions. It is
important for such data to be delivered and be
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

The app contains a bunch of authorities each one with a
bunch of users. Each authority that wants to
receive data will need to upload a Public key,
which will then need to get the administration
to approve using some OOB communication.

After the public key is approved the authority
can receive data. The data is encrypted with
the receiving authority public key using
OpenPGP.js *on the client side" and the cipher
is saved to the server. Since the original data
never reaches the server we can be sure that
even if the server was compromised somehow
no sensitive data would be breached.

When a user of the receiving authority logs in
he can choose to submit the authority private key so
it can be used to decrypt the authority data.
