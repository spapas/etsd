import requests, json
from django.utils.translation import ugettext as _
from django.conf import settings


def check_signatures(file, arr_of_number_of_signatures):
    r = requests.post(
        settings.SIGNATURE_CHECKER_URL,
        files={
            "file": file.read(),
        },
        data={"json": "on"},
    )
    file.seek(0)

    j = json.loads(r.content)

    if j["message"] == "OK":
        sinfo = j.get("pdfSignatureInfo")
        if len(sinfo) in arr_of_number_of_signatures:
            for info in sinfo:
                if not info["signatureVerified"] == "YES" or info["isSelfSigned"]:
                    return _(
                        "Το αρχείο περιέχει εσφαλμένη υπογραφή! Πρέπει να υπογραφεί ξανά!"
                    )
        else:
            return _(
                "Το αρχείο που ανεβάζετε δεν έχει τον κατάλληλο αριθμό υπογραφών. Το αρχείο πρέπει να έχει {0} υπογραφές και έχει {1}."
            ).format(
                _(" ή ").join(str(x) for x in arr_of_number_of_signatures), len(sinfo)
            )

    else:
        if "contain versioninfo" in j["message"]:
            return _("Το αρχείο πρέπει να είναι μορφής PDF!")
        if "exception" in j["message"]:
            return _(
                "Σφάλμα κατά την ανάγνωση του αρχείου! Παρακαλούμε επιβεβαιώσατε ότι είναι κατάλληλης μορφής και έχει υπογραφεί με το σωστό πρόγραμμα!"
            )
        return j["message"]
