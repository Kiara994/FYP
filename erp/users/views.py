from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from erp.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()

#
# class UserRedirectView(LoginRequiredMixin, RedirectView):
#     permanent = False
#
#     def get(self, request, *args, **kwargs):
#         user = self.request.user  # Get logged-in user
#
#         if not user.has_completed_registration:
#             if user.is_doctor:
#                 return "/doctor/registration/"  # Redirect to Doctor Registration
#             elif user.is_patient:
#                 return "/patient/registration/"  # Redirect to Patient Registration
#             elif user.is_staff_member:
#                 return "/doctor/staff_registration/"  # Redirect to Staff Registration
#
#         if user.is_superuser:
#             return redirect("admin:index")  # Django Admin Panel
#
#         if user.is_doctor and user.is_patient:
#             return redirect("dashboard:doctor_patient")  # If the user is both doctor and patient
#         elif user.is_doctor:
#             return redirect("dashboard:doctor")  # Doctor Dashboard
#         elif user.is_patient:
#             return redirect("dashboard:patient")  # Patient Dashboard
#         elif user.is_staff_member:
#             return redirect("dashboard:staff")  # Staff Dashboard
#
#         return redirect("account_login")  # If no role assigned, send to login page
#
#
# user_redirect_view = UserRedirectView.as_view()


#custom given
class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})
user_redirect_view = UserRedirectView.as_view()















############################    CUSTOMIZATION ADDED HERE



# def dashboard_redirect(request):
#     user = request.user
#
#     if not user.is_authenticated:  # ✅ Ensure user is logged in
#         return redirect("account_login")
#
#     if not user.is_registered:
#         return redirect("user_registration")  # URL where users will select their role
#
#
#     if user.is_superuser:
#         return redirect("admin_dashboard")
#     elif getattr(user, "is_doctor", False):
#         return redirect(reverse("doctor:dashboard"))
#     elif getattr(user, "is_patient", False):
#         return redirect(reverse("patient:dashboard"))
#     elif getattr(user, "is_staff_member", False):
#         return redirect("staff_dashboard")
#
#         # ✅ If no role is assigned, send to a "role selection" page instead of looping
#     return redirect("users:assign_role")  # Create a simple page where users select a role



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard_redirect(request):
#     user = request.user
#
#     # If the user is not registered, send them to their relevant registration page
#     if not user.is_registered:
#         if user.is_doctor:
#             return redirect("doctor:register")  # Redirect to doctor registration
#         elif user.is_patient:
#             return redirect("patient:register")  # Redirect to patient registration
#         elif user.is_staff_member:
#             return redirect("doctor:staff_register")  # Redirect to staff registration
#         else:
#             return redirect("users:assign_role")  # If no role is assigned, select one
#
#     # If registered, redirect to their respective dashboard
#     if user.is_doctor:
#         return redirect("doctor:dashboard")
#     elif user.is_patient:
#         return redirect("patient:dashboard")
#     elif user.is_staff_member:
#         return redirect("doctor:staff_dashboard")
#
#     return redirect("home")  # Default homepage if no role
#
#
from django.views.decorators.http import require_http_methods

# @login_required
# @require_http_methods(["GET", "POST"])
# @csrf_protect
# def dashboard_redirect(request):
#     user = request.user
#
#     # Prevent redirection loop by checking if already on the target page
#     current_path = request.path
#
#     # If the user is not registered, send them to their relevant registration page
#     if not user.is_registered:
#         if user.is_doctor and current_path != "/doctor/register/":
#             return redirect("doctor:register")
#         elif user.is_patient and current_path != "/patient/register/":
#             return redirect("patient:register")
#         elif user.is_staff_member and current_path != "/doctor/staff_register/":
#             return redirect("doctor:staff_register")
#         elif current_path != "/users/assign_role/":
#             return redirect("users:assign_role")
#
#     # If registered, redirect to their respective dashboard (avoiding repeated redirects)
#     if user.is_doctor and current_path != "/doctor/dashboard/":
#         return redirect("doctor:dashboard")
#     elif user.is_patient and current_path != "/patient/dashboard/":
#         return redirect("patient:dashboard")
#     elif user.is_staff_member and current_path != "/doctor/staff_dashboard/":
#         return redirect("doctor:staff_dashboard")
#
#     return redirect("home")  # Default homepage if no role



#
# @login_required
# @require_http_methods(["GET", "POST"])
# @csrf_protect
# def dashboard_redirect(request):
    # user = request.user
    #
    # # Prevent redirection loop by ensuring is_registered is properly checked
    # if not hasattr(user, "is_registered") or not user.is_registered:
    #     if user.is_doctor:
    #         return redirect("doctor:register")
    #     elif user.is_patient:
    #         return redirect("patient:register")
    #     elif user.is_staff_member:
    #         return redirect("doctor:staff_register")
    #     return redirect("users:assign_role")
    #
    # # Stop redirection if already on the correct dashboard
    # if user.is_doctor and request.path != "/doctor/dashboard/":
    #     return redirect("doctor:dashboard")
    # elif user.is_patient and request.path != "/patient/dashboard/":
    #     return redirect("patient:dashboard")
    # elif user.is_staff_member and request.path != "/doctor/staff_dashboard/":
    #     return redirect("doctor:staff_dashboard")
    #
    # return redirect("home")  # Default homepage if no role

@login_required
def dashboard_redirect(request):
    user = request.user

    # Debugging logs
    print(f"User: {user.email}, is_authenticated: {user.is_authenticated}, is_registered: {user.is_registered}, Roles: {user.get_roles()}")

    # If user is not registered, send them to their registration page
    if not user.is_registered:
        if user.is_doctor:
            return redirect("doctor:register")
        elif user.is_patient:
            return redirect("patient:register")
        elif user.is_staff_member:
            return redirect("doctor:staff_register")
        return redirect("users:assign_role")

    # Ensure that already registered users are not sent in a loop
    if user.is_patient and request.path != "/patient/dashboard/":
        return redirect("patient:dashboard")
    elif user.is_doctor and request.path != "/doctor/dashboard/":
        return redirect("doctor:dashboard")
    elif user.is_staff_member and request.path != "/doctor/staff_dashboard/":
        return redirect("doctor:staff_dashboard")

    return redirect("home")  # Default homepage if no role





def assign_role_view(request):
    # return render(request, "users/assign_role.html")
    user = request.user

    if request.method == "POST":
        role = request.POST.get("role")

        if role == "doctor":
            user.is_doctor = True
        elif role == "patient":
            user.is_patient = True
        elif role == "staff":
            user.is_staff_member = True

        user.save()
        return redirect(reverse("users:detail", kwargs={"pk": user.pk}))

    return render(request, "users/assign_role.html")
