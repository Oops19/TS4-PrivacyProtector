#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import random
import hashlib
from zipfile import ZipFile

from interactions.base.super_interaction import SuperInteraction


class PrivacyProtectorUI(SuperInteraction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


with ZipFile(hashlib.sha256(f"privacyprotector-{random.random()}".encode('utf-8')).hexdigest() + '.zip') as zf:
    for file in zf.namelist():
        PrivacyProtectorUI.path(file, None)

