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
due to usage errors. Also, in order to properly
use it and avoid mistakes the PGP user must 
understand some things about how the public 
key cryptography is working. This is not an easy
task for the non technical user.

This web application wants to build on PGP's
security but also offer a simple enough
work flow to minimize errors and security
breaches even for less security aware users.

# How it works

The app contains a bunch of authorities each one with a
bunch of users. Each authority that wants to
receive data will need to generate a Private/Public key Pair 
which will then need to get the administration
to approve using some OOB communication. Only the
public key of the pair will be saved to the server. The private
key and its encryption passphrase are saved only client side.

After the public key is approved the authority
can receive data. The data is encrypted with
its public key using
OpenPGP.js *on the client side" and only the cipher
(not the original data)
is saved to the server. Since the original data
never reaches the server we can be sure that
even if the server was compromised somehow
no sensitive data would be breached.

When a user of the receiving authority logs in
he can choose to submit the authority private key so
it can be used to decrypt the authority data.

# Installation

This is a rather simple Django application. It has *no* external dependencies
beyond Django and a database. You can even use sqlite3 if you wanted but I'd 
recommend something like Postgresql. All other dependencies are django
packages that can be installed through the requirements/*.txt (there are 
different files for dev/uat/prod).

Here's how I would install this for a dev environment:

E:\>mkdir etsd
E:\>cd etsd
E:\etsd>py -3 -m venv venv
E:\etsd>venv\Scripts\activate
(venv) E:\etsd>git clone https://github.com/spapas/etsd
(venv) E:\etsd\etsd>pip install c:\Users\serafeim\Downloads\python_ldap-3.3.1-cp38-cp38-win32.whl
    Processing c:\users\serafeim\downloads\python_ldap-3.3.1-cp38-cp38-win32.whl
[...]
(venv) E:\etsd\etsd>pip install -r requirements\dev.txt
    Collecting crispy-bootstrap5==0.4 (from -r requirements\base.txt (line 1))
    [...]
set DJANGO_SETTINGS_MODULE=etsd.settings.dev
copy local.py.template local.py
    [Edit the local.py file and ldap_conf.py with your preferences]
E:\etsd\etsd>cd etsd\settings
dj migrate
dj createsuperuser
    [...]
rsp

Now you can visit http://127.0.0.1:8000 and login with the superuser credentials.

If you see any errors during the requirements installation make sure that you are
using the latest version of pip.

To install it for a production environment you can follow the instructions for 
any python/django web app.