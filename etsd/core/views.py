from django.http.response import HttpResponseRedirect
from django.views.generic import UpdateView, TemplateView, CreateView, ListView
from authorities.models import Authority
from etsd.msgs.filters import MessageFilter
from .forms import AuthorityUsersModelForm
from django.contrib import messages
from django.utils.translation import gettext as _
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
import django_filters
from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap5
import django_tables2 as tables
from django_tables2.utils import A
from django_tables2 import RequestConfig


def filter_has_active_key(queryset, name, value):
    if value == True:
        return queryset.filter(publickey__status="ACTIVE").distinct()
    else:
        return queryset.exclude(publickey__status="ACTIVE").distinct()


def filter_has_users(queryset, name, value):
    if value == True:
        return queryset.exclude(users__id__isnull=True).distinct()
    else:
        return queryset.filter(users__id__isnull=True).distinct()


class AuthorityFilter(django_filters.FilterSet):
    has_active_key = django_filters.BooleanFilter(
        label="Has active key", field_name="foo", method=filter_has_active_key
    )
    has_users = django_filters.BooleanFilter(
        label="Has users", field_name="foo", method=filter_has_users
    )

    class Meta:
        model = Authority
        fields = {
            "name": ["icontains"],
            "kind": ["exact"],
            "is_active": ["exact"],
            # "users__username": ["isnull"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.form["users__username__isnull"].label = "Χωρίς χρήστες"


class AuthorityTable(ColumnShiftTableBootstrap5):
    id = tables.LinkColumn(
        "authority_view",
        args=[A("pk")],
        attrs={"a": {"class": "btn btn-info btn-sm"}},
    )
    users = tables.TemplateColumn(
        "{% for u in record.users.all %}{{ u.username }}{% if not forloop.last %}, {% endif %}{% endfor %}"
    )
    # keys = tables.TemplateColumn("{% for u in record.publickeys_set.all %}{{ u.approved_on }}{% if not forloop.last %}, {% endif %}{% endfor %}")

    class Meta:
        model = Authority
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"
        fields = ("id", "kind", "name", "email", "is_active", "users")


class AuthorityListView(ListView):
    model = Authority
    context_object_name = "authorities"

    def get_queryset(self):

        qs = (
            super()
            .get_queryset()
            .prefetch_related("users", "publickey_set")
            .select_related("kind")
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        qs = self.get_queryset()
        self.filter = AuthorityFilter(self.request.GET, qs)
        self.table = table = AuthorityTable(self.filter.qs)

        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["filter"] = self.filter
        context["table"] = self.table
        return context


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
                    recipient_list=[usr.email for usr in added_users if usr.email]
                    + [auth.email],
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
                    recipient_list=[usr.email for usr in removed_users if usr.email]
                    + [auth.email],
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


def send_test_mail(request):
    from django.core.mail import send_mail
    from django.conf import settings
    from django.http import HttpResponse

    send_mail(
        "TEST FROM ETSD",
        "TEST",
        settings.DEFAULT_FROM_EMAIL,
        [x[1] for x in settings.ADMINS],
    )
    return HttpResponse("OK")


from simple_stats import get_stats
from etsd.msgs import models
from authorities import models as auth_models
from etsd.keys import models as key_models
from django.db.models import OuterRef, Subquery, Exists, F
from django.contrib.auth import get_user_model

User = get_user_model()

STATS_CFG = [
    {
        "label": "Total Messages",
        "kind": "query_aggregate_single",
        "method": "count",
        "field": "id",
    },
    {
        "label": "Per year",
        "kind": "query_aggregate",
        "method": "count",
        "field": "protocol_year",
    },
    {
        "label": "Per status",
        "kind": "choice_aggregate",
        "method": "count",
        "field": "status",
        "choices": models.MESSAGE_STATUS_CHOICES,
    },
    {
        "label": "Per kind",
        "kind": "choice_aggregate",
        "method": "count",
        "field": "kind",
        "choices": models.MESSAGE_KIND_CHOICES,
    },
    {
        "label": "Per sending authority",
        "kind": "query_aggregate",
        "method": "count",
        "field": "sender",
    },
    {
        "label": "Per recipient authority",
        "kind": "query_aggregate",
        "method": "count",
        "field": "recipient",
    },
    {
        "label": "Per cc authority",
        "kind": "query_aggregate",
        "method": "count",
        "field": "cc",
    },
    {
        "label": "Avg read time",
        "kind": "query_aggregate_single",
        "method": "avg",
        "field": "read_time",
    },
    {
        "label": "Max read time",
        "kind": "query_aggregate_single",
        "method": "max",
        "field": "read_time",
    },
    {
        "label": "Min read time",
        "kind": "query_aggregate_single",
        "method": "min",
        "field": "read_time",
    },
]

AUTH_STATS_CFG = [
    {
        "label": "Total authorities",
        "kind": "query_aggregate_single",
        "method": "count",
        "field": "id",
    },
    {
        "label": "Per active",
        "kind": "query_aggregate",
        "method": "count",
        "field": "is_active",
    },
    {
        "label": "Per kind",
        "kind": "query_aggregate",
        "method": "count",
        "field": "kind__name",
    },
    {
        "label": "Per has users",
        "kind": "query_aggregate",
        "method": "count",
        "field": "has_users",
    },
    {
        "label": "Per has active key",
        "kind": "query_aggregate",
        "method": "count",
        "field": "has_active_key",
    },
]


class StatsMessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(
        label="Sender", field_name="sender", lookup_expr="icontains"
    )
    recipient = django_filters.CharFilter(
        label="Recipient", field_name="recipient", lookup_expr="icontains"
    )
    cc = django_filters.CharFilter(label="CC", field_name="cc", lookup_expr="icontains")

    class Meta:
        model = models.Message
        fields = {
            "kind": ["exact"],
            "status": ["exact"],
            "protocol_year": ["exact"],
            "sent_on": ["exact", "month", "year"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StatsView(TemplateView):
    template_name = "core/stats.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # TODO: THis query is *not* correct. Please notice that we
        # need to use the [:1] to get only the 1st recipient and cc
        # or else this will break (because the subquery will return multiple results)
        qs = models.Message.objects.all().annotate(
            sender=Subquery(
                models.Participant.objects.filter(
                    message=OuterRef("pk"), kind="SENDER"
                ).values("authority__name")
            ),
            recipient=Subquery(
                models.Participant.objects.filter(
                    message=OuterRef("pk"), kind="RECIPIENT"
                ).values("authority__name")[:1]
            ),
            cc=Subquery(
                models.Participant.objects.filter(
                    message=OuterRef("pk"), kind="CC"
                ).values("authority__name")[:1]
            ),
            data_access_date=Subquery(
                models.DataAccess.objects.filter(
                    data__message=OuterRef("pk"),
                    participant__kind="RECIPIENT",
                ).values("created_on")[:1]
            ),
            read_time=F("data_access_date") - F("sent_on"),
        )

        filter = StatsMessageFilter(self.request.GET, qs)

        stats = get_stats(filter.qs, STATS_CFG)

        auth_qs = auth_models.Authority.objects.all().annotate(
            has_users=Exists(User.objects.filter(authorities__id=OuterRef("pk"))),
            has_active_key=Exists(
                key_models.PublicKey.objects.filter(
                    status="ACTIVE", authority__id=OuterRef("pk")
                )
            ),
        )
        auth_stats = get_stats(auth_qs, AUTH_STATS_CFG)
        ctx.update(
            {
                "stats": stats,
                "auth_stats": auth_stats,
                "filter": filter,
            }
        )

        return ctx
