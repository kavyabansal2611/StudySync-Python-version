from resend import Emails
from core.config import settings

resend_api_key=settings.RESEND_API_KEY
def send_verification_email(to_email: str, token: str)->None:
    verification_url=(
        f"{settings.FRONTEND_URL}",
        f"/verify-email?token={token}"
    )

    Emails.send({
        "from":settings.EMAIL_FROM
        "to":to_email
        "subject":"Verify your StudySync Account"
        "html":f"""
        <h2>Welcome to StudySync!</h2>

        <p>
            Click the button below to verify
            your email address.
        </p>

        <a href="{verification_url}">
            Verify Email
        </a>

        <p>
            If you didn't create this account,
            please ignore this email.
        </p>
        """
    }
    );

    def password_reset_mail(to_email:str,token:str)->None:
        reset_url=(
            f"{settings.FRONTEND_URL}",
            f"/reset-password?token={token}"
        )
        Emails.send({
            "from":settings.EMAIL_FROM
            "to":to_email
            "subject":"Reset your StudySync account password"
            "html":f"""
            <h2>Password Reset</h2>

            <p>
            Click below to reset your password.
            </p>

            <a href="{reset_url}">
            Reset Password
            </a>
        """

        })
        


