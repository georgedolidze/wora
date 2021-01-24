import smtplib, ssl
from getpass import getpass

port = 25252
password = getpass()
sender_email = 'gdolidze@cenic.org'
receiver_email = 'gdolidze@cenic.org'
message = 'This is the message of the email'
host = 'mail2.cenic.org'

# Create a secure SSL context
context = ssl._create_unverified_context()

_DEFAULT_CIPHERS = (
'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
'!eNULL:!MD5')

#def encrypt_check():
smtp_server = smtplib.SMTP(host, port=port)
# only TLSv1 or higher
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.options |= ssl.OP_NO_SSLv2
context.options |= ssl.OP_NO_SSLv3
context.set_ciphers(_DEFAULT_CIPHERS)
context.set_default_verify_paths()
context.verify_mode = ssl.CERT_REQUIRED

def encrypter(smtp_server):
    if smtp_server.starttls(context=context)[0] != 220:
        return False # cancel if connection is not encrypted

encrypter(smtp_server)

smtp_server.login(sender_email, password)
smtp_server.sendmail(sender_email, receiver_email, message)

#with smtplib.SMTP("mail2.cenic.org", port) as server:
#    server.starttls(context=context)
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message)  
