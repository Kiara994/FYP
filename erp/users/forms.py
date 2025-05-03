from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField, ChoiceField,MultipleChoiceField, CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

# SignupForm = import_string("allauth.account.forms.SignupForm")
# SocialSignupForm = import_string("allauth.socialaccount.forms.SignupForm")
from .models import User

#
# def get_signup_form():
#     return import_string("allauth.account.forms.SignupForm")
#
# def get_social_signup_form():
#     return import_string("allauth.socialaccount.forms.SignupForm")




class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


# from django import forms
# from allauth.account.forms import SignupForm
# from .models import User


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign-up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    #added myseldddd
    #
    # ROLE_CHOICES = [
    #     ('doctor', 'Doctor'),
    #     ('patient', 'Patient'),
    #     ('staff', 'Staff Member'),
    # ]
    #
    # role = ChoiceField(choices=ROLE_CHOICES, required=True, label="Register as")
    #
    # def save(self, request):
    #     user = super().save(request)
    #     role = self.cleaned_data['role']
    #
    #     if role == 'doctor':
    #         user.is_doctor = True
    #     elif role == 'patient':
    #         user.is_patient = True
    #     elif role == 'staff':
    #         user.is_staff_member = True
    #
    #     user.save()
    #     return user


class UserSocialSignupForm(SignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """





####################      CUSTOMIZATION   ##########################
# class CustomSignupForm(SignupForm):
#     ROLE_CHOICES=[
#         ('patient', 'Patient'),
#         ('doctor', 'Doctor'),
#         ('staff', 'Staff'),
#     ]
#
#     roles=MultipleChoiceField(
#         choices=ROLE_CHOICES,
#         widget=CheckboxSelectMultiple,
#         required=True
#     )
#
#     def save(self,request):
#         user=super().save(request)
#         selected_roles = self.cleaned_data.get('roles', [])
#         # Assign roles to the user model
#
#         print("Selected Roles:", selected_roles)
#
#         if 'patient' in selected_roles:
#             user.is_patient = True
#         if 'doctor' in selected_roles:
#             user.is_doctor = True
#         if 'staff' in selected_roles:
#             user.is_staff_member = True
#
#
#         user.save()
#         return user



class CustomSignupForm(SignupForm):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
    ]

    roles = MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=CheckboxSelectMultiple,
        required=True
    )

    def save(self, request):
        user = super().save(request)
        selected_roles = self.cleaned_data.get('roles', [])

        print("Selected Roles:", selected_roles)

        if 'patient' in selected_roles:
            user.is_patient = True
        if 'doctor' in selected_roles:
            user.is_doctor = True
        if 'staff' in selected_roles:
            user.is_staff_member = True

        #user.is_registered = True  # Mark the user as registered
        user.save()
        return user
