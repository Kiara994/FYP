from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import user_detail_view, dashboard_redirect, assign_role_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    # path("~redirect/", view=user_redirect_view, name="redirect"), this was fdefault one bottom one added by me
    path("dashboard_redirect/", dashboard_redirect, name="dashboard_redirect"),#added by me
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("assign-role/", assign_role_view, name="assign_role"),
]
