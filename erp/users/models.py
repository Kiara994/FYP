
# from typing import ClassVar
#
# from django.contrib.auth.models import AbstractUser
# from django.db.models import CharField
# from django.db.models import EmailField,BooleanField
# from django.urls import reverse
# from django.utils.translation import gettext_lazy as _
#
# from .managers import UserManager





#
# class User(AbstractUser):
#     """
#     Default custom user model for Hospitex ERP.
#     If adding fields that need to be filled at user signup,
#     check forms.SignupForm and forms.SocialSignupForms accordingly.
#     """
#
#     # First and last name do not cover name patterns around the globe
#     name = CharField(_("Name of User"), blank=True, max_length=255)
#     first_name = None  # type: ignore[assignment]
#     last_name = None  # type: ignore[assignment]
#     email = EmailField(_("email address"), unique=True)
#     username = None  # type: ignore[assignment]
#
#
#     is_doctor = BooleanField(default=False)
#     is_patient = BooleanField(default=False)
#     is_staff_member=BooleanField(default=False)
#
#     has_completed_registration = BooleanField(default=False)
#
#
#
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     objects: ClassVar[UserManager] = UserManager()
#
#     class Meta:
#         app_label = "users"  # Ensure this matches your app directory
#     def get_absolute_url(self) -> str:
#         """Get URL for user's detail view.
#
#         Returns:
#             str: URL for user detail.
#
#         """
#         return reverse("users:detail", kwargs={"pk": self.id})
#


















#
# DEFAULT GIVEN
#
# class User(AbstractUser):
#     """
#     Default custom user model for Hospitex ERP.
#     If adding fields that need to be filled at user signup,
#     check forms.SignupForm and forms.SocialSignupForms accordingly.
#     """
#
#     # First and last name do not cover name patterns around the globe
#     name = CharField(_("Name of User"), blank=True, max_length=255)
#     first_name = None  # type: ignore[assignment]
#     last_name = None  # type: ignore[assignment]
#     email = EmailField(_("email address"), unique=True)
#     username = None  # type: ignore[assignment]
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     objects: ClassVar[UserManager] = UserManager()
#
#     def get_absolute_url(self) -> str:
#         """Get URL for user's detail view.
#
#         Returns:
#             str: URL for user detail.
#
#         """
#         return reverse("users:detail", kwargs={"pk": self.id})






#######################       CUSTOMIZATION


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

# class User(AbstractUser):
#     """
#     Custom user model for Hospitex ERP.
#     Users log in with email instead of username.
#     """
#
#     name = models.CharField(_("Name of User"), blank=True, max_length=255)
#     first_name = None  # type: ignore[assignment]
#     last_name = None  # type: ignore[assignment]
#     email = models.EmailField(_("email address"), unique=True)
#     username = None  # type: ignore[assignment]
#
#     is_doctor = models.BooleanField(default=False)       # Doctor role
#     is_patient = models.BooleanField(default=False)      # Patient role
#     is_staff_member = models.BooleanField(default=False) # Staff role
#     is_registered = models.BooleanField(default=False)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     def get_absolute_url(self) -> str:
#         """Get URL for user's detail view."""
#         return reverse("users:detail", kwargs={"pk": self.id})
#
#     def get_roles(self):
#         """Returns the user's roles as a list."""
#         roles = []
#         if self.is_doctor:
#             roles.append("Doctor")
#         if self.is_patient:
#             roles.append("Patient")
#         if self.is_staff_member:
#             roles.append("Staff")
#         return roles if roles else ["No Role Assigned"]


#######             Previous code


# class User(AbstractUser):
#     """
#     Custom user model for Hospitex ERP.
#     Users log in with email instead of username.
#     """
#
#     name = models.CharField(_("Name of User"), blank=True, max_length=255)
#     first_name = None  # type: ignore[assignment]
#     last_name = None  # type: ignore[assignment]
#     email = models.EmailField(_("email address"), unique=True)
#     username = None  # type: ignore[assignment]
#
#     is_doctor = models.BooleanField(default=False)       # Doctor role
#     is_patient = models.BooleanField(default=False)      # Patient role
#     is_staff_member = models.BooleanField(default=False) # Staff role
#     is_registered = models.BooleanField(default=False)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     def get_absolute_url(self) -> str:
#         """Get URL for user's detail view."""
#         return reverse("users:detail", kwargs={"pk": self.id})
#
#     def get_roles(self):
#         """Returns the user's roles as a list."""
#         roles = []
#         if self.is_doctor:
#             roles.append("Doctor")
#         if self.is_patient:
#             roles.append("Patient")
#         if self.is_staff_member:
#             roles.append("Staff")
#         return roles if roles else ["No Role Assigned"]





###### error checking code



class User(AbstractUser):
    """
    Custom user model for Hospitex ERP.
    Users log in with email instead of username.
    """

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    is_doctor = models.BooleanField(default=False)       # Doctor role
    is_patient = models.BooleanField(default=False)      # Patient role
    is_staff_member = models.BooleanField(default=False) # Staff role
    is_registered = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view."""
        return reverse("users:detail", kwargs={"pk": self.id})

    def get_roles(self):
        """Returns the user's roles as a list."""
        roles = []
        if self.is_doctor:
            roles.append("Doctor")
        if self.is_patient:
            roles.append("Patient")
        if self.is_staff_member:
            roles.append("Staff")
        return roles if roles else ["No Role Assigned"]
