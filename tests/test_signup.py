import re

from playwright.sync_api import Page
from tests.pages.auth import SignupPage, ConfirmationPage
from app.models import UserProfile
from django.core import mail
from allauth.account.models import EmailAddress

def test_signup(page: Page, user_data: dict):
    page.goto("/")
    signup_page = SignupPage(page)
    # signup_page.email_field.fill("test@example.com")
    # signup_page.password_field.fill("example_password")
    # signup_page.signup_button.click()

    # Alternative

    signup_page.complete_signup_form(user_data["email"], user_data["password"])

    confirmation_link = re.search(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        mail.outbox[0].body,
    ).group()

    page.goto(confirmation_link)

    confirmation_page = ConfirmationPage(page)
    confirmation_page.confirm_button.click()

    user = UserProfile.objects.get(email="test@example.com")
    email_address = EmailAddress.objects.get(user=user, email="test@example.com")
    assert email_address.verified