#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import random
import hashlib
from zipfile import ZipFile

with ZipFile(hashlib.sha256(f"privacyprotector-{random.random()}".encode('utf-8')).hexdigest() + '.zip') as zf:
    for file in zf.namelist():
        if file.endswith('.pyc'):
            privacyprotector.launch(file)
