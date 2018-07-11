from django.views.generic.base import TemplateView
from django.shortcuts import render
from ui.models import User


class PasswordResetDoneView(TemplateView):
    model = User
    template_name = "account/password_reset_done.html"

    def get(self, request, *args, **kwargs):
        context = {"model_name": "User"}
        superusers = User.objects.filter(is_superuser=True)
        # get the first super user email information
        context["email_info"] = 'mailto:' + superusers[0].email if superusers else ''
        return render(request, self.template_name, context)


password_reset_done = PasswordResetDoneView.as_view()
