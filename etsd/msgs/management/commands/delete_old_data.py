from collections import defaultdict
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Exists, OuterRef
from etsd.msgs import models
from django.core.mail import send_mail
from etsd.core.utils import send_mail_body
from etsd.users.utils import get_authority_users_emails
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = "Delete data  older than a year (from the date the message was sent). Notify authorities for data to be deleted after 10 days."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no_dry",
            action="store_true",
            default=False,
            help="Include this option to actually delete",
        )

    def handle(self, *args, **kwargs):
        three_years_before = timezone.now() - timezone.timedelta(days=1095)
        three_years_before_p10 = three_years_before + timezone.timedelta(days=10)
        self.stdout.write("Will delete messages older than: {}".format(three_years_before))
        self.stdout.write(
            "Will notify for messages older than: {}".format(three_years_before_p10)
        )

        messages_to_delete = models.Message.objects.filter(
            Exists(models.CipherData.objects.filter(data__message=OuterRef("pk"))),
            sent_on__lte=three_years_before,
        )

        del_cdata = models.CipherData.objects.filter(
            data__message__in=messages_to_delete
        )

        if del_cdata:
            self.stdout.write(
                self.style.WARNING("Data from the following messages will be deleted:")
            )
            self.stdout.write(
                "{}".format(", ".join(str(x) for x in messages_to_delete))
            )
            self.stdout.write(self.style.WARNING("Data to be deleted:"))
            self.stdout.write("{}".format(", ".join(str(x) for x in del_cdata)))

        messages_to_notify = models.Message.objects.filter(
            Exists(models.CipherData.objects.filter(data__message=OuterRef("pk"))),
            sent_on__lte=three_years_before_p10,
        )

        participants_to_notify = []
        for message in messages_to_notify:
            for participant in models.Participant.objects.filter(message=message):
                participants_to_notify.append((participant.authority, message))

        participants_to_notify_dict = defaultdict(list)
        for k, v in participants_to_notify:
            participants_to_notify_dict[k].append(v)

        if messages_to_notify:
            self.stdout.write(
                self.style.SUCCESS("Messages to be deleted within 10 days:")
            )
            self.stdout.write(
                "{}".format(", ".join(str(x) for x in messages_to_notify))
            )
            self.stdout.write(self.style.SUCCESS("Participants to be notified:"))
            for k in participants_to_notify_dict:
                self.stdout.write("{0}: {1}".format(k, k.email))

        if kwargs["no_dry"]:
            del_cdata.delete()

        for k in participants_to_notify_dict:
            email_body = send_mail_body(
                "msgs/emails/notify_data_deletion.txt",
                dict(
                    messages=participants_to_notify_dict[k],
                    three_years_before_p10=three_years_before_p10,
                ),
            )
            recipients = get_authority_users_emails(k)
            if kwargs["no_dry"] and len(recipients) > 0:
                send_mail(
                    subject=_("[ETSD] Old message data will be deleted"),
                    message=email_body,
                    from_email="noreply@hcg.gr",
                    recipient_list=recipients,
                    fail_silently=False,
                )
            else:
                self.stdout.write(
                    "Will send emails to: {} for authority {}".format(
                        ",".join(recipients) or "-", k
                    )
                )
                self.stdout.write(email_body)
                self.stdout.write("--------------")

        if kwargs["no_dry"]:
            self.stdout.write(self.style.SUCCESS("Operations completed."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Run command with --no_dry to complete above operations."
                )
            )
