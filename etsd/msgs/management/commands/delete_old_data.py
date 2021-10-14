from collections import defaultdict
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Exists, OuterRef
from etsd.msgs import models
from django.core.mail import send_mail
from etsd.core.utils import send_mail_body
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    help = "Delete data  older than a year (from the date the message was sent). Notify authorities for data to be deleted after 10 days."

    def handle(self, *args, **kwargs):
        one_year_before = timezone.now() - timezone.timedelta(days=365)
        messages_to_delete = models.Message.objects.filter(
            Exists(models.CipherData.objects.filter(data__message = OuterRef('pk'))),
            sent_on__lte=one_year_before
        )

        del_cdata = models.CipherData.objects.filter(data__message__in=messages_to_delete)

        if del_cdata:
            self.stdout.write(self.style.WARNING("Data from the following messages will be deleted:"))
            self.stdout.write("%s" %messages_to_delete)
            for cdata in del_cdata:
                cdata.delete()
            self.stdout.write(self.style.WARNING("Deleted data:"))
            self.stdout.write("%s" %del_cdata)


        messages_to_notify = models.Message.objects.filter(
            Exists(models.CipherData.objects.filter(data__message = OuterRef('pk'))),
            sent_on__lte=(one_year_before + timezone.timedelta(days=10))
        )

        participants_to_notify= []
        for message in messages_to_notify:
            for participant in models.Participant.objects.filter(message=message):
                participants_to_notify.append((participant.authority,message))

        participants_to_notify_dict = defaultdict(list)
        for k, v in participants_to_notify:
            participants_to_notify_dict[k].append(v)

        for k in participants_to_notify_dict:
            email_body = send_mail_body(
                "msgs/emails/notify_data_deletion.txt",
                dict(messages=participants_to_notify_dict[k]),
            )
            send_mail(
                subject=_("Old message data to be deleted"),
                message=email_body,
                from_email="noreply@hcg.gr",
                recipient_list=[k.email],
                fail_silently=False,
            )

        if messages_to_notify:
            self.stdout.write(self.style.SUCCESS("Messages to be deleted within 10 days (notified participants):"))
            self.stdout.write("%s" %messages_to_notify)
