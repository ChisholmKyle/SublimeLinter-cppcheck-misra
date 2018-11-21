#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Kyle Chisholm
# Copyright (c) 2016 Kyle Chisholm
#
# License: MIT
#

"""This module exports the CppcheckMisra plugin class."""

import re
import os
from SublimeLinter.lint import Linter, util

OUTPUT_RE = re.compile(r'\[[^:]*:(?P<line>\d+)\] (?P<message>.+)')


class CppcheckMisra(Linter):
    """Provides an interface to cppcheck with MISRA C 2012."""

    name = 'cppcheck-misra'

    tempfile_suffix = 'c'

    cmd = 'cppcheck-misra --cppcheck-opts ${args} ${temp_file}'

    defaults = {
        'executable': os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'scripts',
            'cppcheck-misra'),
        'selector': 'source.c',
        'args': [
            '--max-configs=1'
        ],
        '--suppress-rules,': [],
        '--misra-addon': '/usr/local/share/CppCheck/addons/misra.py',
        '--rule-texts': ''
    }

    regex = OUTPUT_RE
    multiline = False
    error_stream = util.STREAM_STDERR
