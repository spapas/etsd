from django.http.response import HttpResponseRedirect
from django.views.generic import UpdateView, TemplateView, CreateView
from authorities.models import Authority
from .forms import AuthorityUsersModelForm
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from dal import autocomplete
from django.db.models import Q
from dj_rest_auth.views import LogoutView, LoginView
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from etsd.users.models import UserManagementLog
from django.core.mail import send_mail
from etsd.core.utils import send_mail_body

  

class AuthorityCreateView(CreateView):
    model = Authority
    fields = (
        "name",
        "kind",
        "is_active",
        "email",
    )


class AuthorityUpdateView(UpdateView):
    model = Authority
    context_object_name = "authority"
    fields = (
        "name",
        "kind",
        "is_active",
        "email",
    )


class AuthorityEditUsersView(
    UpdateView,
):
    model = Authority
    form_class = AuthorityUsersModelForm
    template_name = "core/edit_authority_data.html"

    def get_form_kwargs(self):
        kwargs = super(AuthorityEditUsersView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user_management_log"] = (
            self.object.usermanagementlog_set.all()
            .order_by("-created_on")
            .select_related("created_by")
        )
        return ctx

    def form_valid(self, form):
        new_users = form.cleaned_data["users"]
        auth = form.instance
        initial_users = auth.users.all()
        added_users = set(new_users).difference(set(initial_users))
        removed_users = set(initial_users).difference(set(new_users))

        user_permission = Permission.objects.get(
            codename="user", content_type__model="globalpermissionholder"
        )
        for usr in added_users:
            usr.user_permissions.add(user_permission)
        for usr in removed_users:
            usr.user_permissions.remove(user_permission)

        form.save()
        if added_users or removed_users:
            if added_users:
                email_body = send_mail_body(
                    "core/emails/edited_users.txt",
                    dict(
                        action=_("added"),
                        authority=auth,
                        action_user=self.request.user,
                    ),
                )
                send_mail(
                    subject=_("Added as user in ETSD"),
                    message=email_body,
                    from_email="noreply@hcg.gr",
                    recipient_list=[usr.email for usr in added_users if usr.email],
                    fail_silently=False,
                )
            if removed_users:
                email_body = send_mail_body(
                    "core/emails/edited_users.txt",
                    dict(
                        action=_("removed"),
                        authority=auth,
                        action_user=self.request.user,
                    ),
                )
                send_mail(
                    subject=_("Removed as a user in ETSD"),
                    message=email_body,
                    from_email="noreply@hcg.gr",
                    recipient_list=[usr.email for usr in removed_users if usr.email],
                    fail_silently=False,
                )
            uml = UserManagementLog()
            uml.authority = auth
            uml.added_users = ", ".join(usr.username for usr in added_users)
            uml.removed_users = ", ".join(usr.username for usr in removed_users)
            uml.save()

        messages.add_message(
            self.request, messages.INFO, _("Authority Data successfully updated!")
        )
        return HttpResponseRedirect(self.request.path)


class AuthorityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Authority.objects.none()

        qs = Authority.objects.all().exclude(id=self.request.user.get_authority().id)

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q)
                | Q(code__icontains=self.q)
                | Q(email__icontains=self.q)
            )

        return qs


class HelpTemplateView(TemplateView):
    template_name = "core/help.html"


class RestLogoutView(LogoutView):
    authentication_classes = (authentication.TokenAuthentication,)


class RestLoginView(LoginView):
    def get_response(self):
        user = self.token.user
        if not user.get_authority():
            return Response(
                {"error": _("This user is not associated with any authority!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "token": self.token.key,
                "authority": str(user.get_authority()),
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
