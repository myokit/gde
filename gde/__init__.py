#
# GDE's main module
#
# This file is part of GDE.
# See https://github.com/MichaelClerx/gde for sharing, and licensing details.
#

"""
Graph Data Extractpr

This module provides a gateway to the main GDE components.
"""

#
# Check python version
#
# Hexversion guide:
#  0x   Hex
#  02   PY_MAJOR_VERSION
#  07   PY_MINOR_VERSION
#  0F   PY_MICRO_VERSION, in hex, so 0F is 15, 10 is 16, etc.
#  F    PY_RELEASE_LEVEL, A for alpha, B for beta, C for candidate, F for final
#  0    PY_RELEASE_SERIAL, increments with every release
#
import sys  # noqa
if sys.hexversion < 0x03050000:  # pragma: no cover
    print('GDE Requires Python 3.5 or newer.')
    sys.exit(1)
del(sys)


#
# Version information
#
from ._gde_version import (  # noqa
    __version__,
    __version_tuple__,
)

def version():
    """Returns this copy of GDE's version number."""
    return gde.__version__


#
# Licensing
#

# Full license text
LICENSE = """
BSD 3-Clause License

Copyright (c) 2011-2017 Maastricht University. All rights reserved.
Copyright (c) 2017-2020 University of Oxford. All rights reserved.
 (University of Oxford means the Chancellor, Masters and Scholars of the
  University of Oxford, having an administrative office at Wellington Square,
  Oxford OX1 2JD, UK).
Copyright (c) 2020-2021 University of Nottingham. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""".strip()

# Full license text, html
LICENSE_HTML = """
<h1>Graph Data Extractor (GDE)</h1>
<p>
    BSD 3-Clause License
    <br />
    <br />Copyright (c) 2011-2017 Maastricht University. All rights reserved.
    <br />Copyright (c) 2017-2020 University of Oxford. All rights reserved.
    <br />(University of Oxford means the Chancellor, Masters and Scholars of
    the University of Oxford, having an administrative office at Wellington
    Square, Oxford OX1 2JD, UK).
    <br />Copyright (c) 2020-2021 University of Nottingham. All rights
    reserved.</br>
</p>
<p>
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
</p>
<ul>
    <li>
        <p>
            Redistributions of source code must retain the above copyright
            notice, this list of conditions and the following disclaimer.
        </p>
    </li>
    <li>
        <p>
            Redistributions in binary form must reproduce the above copyright
            notice, this list of conditions and the following disclaimer in the
            documentation and/or other materials provided with the
            distribution.
        </p>
    </li>
    <li>
        <p>
            Neither the name of the copyright holder nor the names of its
            contributors may be used to endorse or promote products derived
            from this software without specific prior written permission.
        </p>
    </li>
</ul>
<p>
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
</p>
""".strip()


#
# Paths
#

# GDE root
import os, inspect  # noqa
try:
    frame = inspect.currentframe()
    DIR_GDE = os.path.abspath(os.path.dirname(inspect.getfile(frame)))
finally:
    # Always manually delete frame
    # https://docs.python.org/2/library/inspect.html#the-interpreter-stack
    del(frame)

# Binary data files
DIR_DATA = os.path.join(DIR_GDE, '_bin')

# Location of user config files
DIR_USER = os.path.join(os.path.expanduser('~'), '.config', 'gde')

# Ensure the user config directory exists and is writable
if os.path.exists(DIR_USER):    # pragma: no cover
    if not os.path.isdir(DIR_USER):
        raise Exception(
            'File or link found in place of user directory: ' + str(DIR_USER))
else:                           # pragma: no cover
    os.makedirs(DIR_USER)

# Don't expose standard libraries as part of GDE
del(os, inspect)


#
# Tools
#

def rmtree(path):
    """
    Version of ``shutil.rmtree`` that handles Windows "access denied" errors
    (when the user is lacking write permissions, but is allowed to set them).
    """
    import shutil

    # From https://stackoverflow.com/questions/2656322
    def onerror(function, path, excinfo):   # pragma: no cover
        if not os.access(path, os.W_OK):
            # Give user write permissions (remove read-only flag)
            os.chmod(path, stat.S_IWUSR)
            function(path)
        else:
            raise

    shutil.rmtree(path, ignore_errors=False, onerror=onerror)


#
# Imports
#
from . import qt    # noqa
from . import gui     # noqa

