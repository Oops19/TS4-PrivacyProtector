#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2025 https://github.com/Oops19
#

import os
import sys

# On Windows remove 'mac' from sys.path to prevent import errors
if sys.platform != "darwin":
    p = os.path.join(os.path.dirname(__file__), "mac")
    if p in sys.path:
        sys.path.remove(p)
