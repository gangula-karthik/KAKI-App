import pyotp, qrcode
from flask import send_file
from flask import session
from firebaseconfig import db_ref
import io, base64

def generate_secret():
    user_secret = pyotp.random_base32()
    users_ref = db_ref.child("users")
    query_result = users_ref.order_by_child('otpsecret').equal_to(user_secret).get()
    if len(query_result) != 0:
        return generate_secret()
    else:
        return user_secret

def generate_qr(user_secret):
    totp = pyotp.TOTP(user_secret)
    provisioning_uri = totp.provisioning_uri(name='', issuer_name='')
    qr_code = qrcode.make(provisioning_uri)
    qr_code.save("qr_code.png")


def otpverify(id,otp):
    # Retrieve the user's secret key from your user database
    user_secret = get_user_id(id,"otpsecret")


    # Verify the OTP
    totp = pyotp.TOTP(user_secret)
    is_valid = totp.verify(otp)

    if is_valid:
        return True
    else:
        return False



def generate_qrurl(user_secret):
    totp = pyotp.TOTP(user_secret)
    provisioning_uri = totp.provisioning_uri(name='', issuer_name='')
    qr_code = qrcode.make(provisioning_uri)

    # Convert the QR code image to a byte array
    qr_byte_array = io.BytesIO()
    qr_code.save(qr_byte_array, format='PNG')
    qr_byte_array.seek(0)

    # Convert the byte array to a base64-encoded string
    qr_base64_data = base64.b64encode(qr_byte_array.read()).decode('utf-8')

    return qr_base64_data