from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import PublicKey
from ....msgs.models import CipherData, Data, Message


class Command(BaseCommand):
    help = 'Delete a lost/compromised private key along with all corresponding cipher data. Takes fingerprint as argument.'

    def add_arguments(self, parser):
        parser.add_argument('fingerprint', type=str, help='The fingerprint of the lost/compromised private key')

    def handle(self, *args, **kwargs):
        fingerp = kwargs["fingerprint"]
        del_key = PublicKey.objects.filter(fingerprint=fingerp).first()
        del_cdata = CipherData.objects.filter(participant_key__public_key=del_key)
        if del_key:
            self.stdout.write("Deleting key with fingerprint: %s of user: %s" %(del_key.fingerprint, del_key.user_id)) 
            del_key.deleted_on = timezone.now()
            del_key.status = "DELETED"
            del_key.save()
            if del_cdata:
                self.stdout.write("Deleted data:")
                for cdata in del_cdata:
                    self.stdout.write("Cipher data: %s , of message: %s" %(cdata.cipher_data, cdata.data.message)) 
                    cdata.delete()
            else:
                self.stdout.write("No cipher data associated with particular key")
        else:
            self.stdout.write("No key with fingerprint: %s in database" %fingerp)
            