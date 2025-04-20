from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Note: If the username is missing in an admin panel that means
#     that the user was signed up via a username or a third party
#     app. To delete to user, add the "username" field in list_displays()
#     in admin.py, delete the user and remove the "username" field

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Alternative for .setdefault()

        # if "is_staff" not in extra_fields:
        #     extra_fields["is_staff"] = True

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have a is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have a is_superuser=True"))
        
        # Alternative

        # extra_fields["is_staff"] = True
        # extra_fields["is_superuser"] = True

        return self.create_user(email, password, **extra_fields)
        