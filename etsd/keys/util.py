import requests, json
from django.utils.translation import gettext as _
from django.conf import settings


def check_signatures(file, arr_of_number_of_signatures):
    if not settings.CHECK_FILE_SIGNATURES:
        return None
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
                    return _("The signature is invalid!")
        else:
            return _(
                "The file you are uploading does not ave the correct number of signatures. It must have {0} signatures but it has {1}."
            ).format(
                _(" or ").join(str(x) for x in arr_of_number_of_signatures), len(sinfo)
            )

    else:
        if "contain versioninfo" in j["message"]:
            return _("This must be a PDF file!")
        if "exception" in j["message"]:
            return _(
                "Error while trying to read the file! Please make sure it has been signed properly."
            )
        return j["message"]
