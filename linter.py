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
import sublime
from shutil import which
from SublimeLinter.lint import Linter, util

OUTPUT_RE = re.compile(r'\[[^:]*:(?P<line>\d+)\] (?P<message>.+)')


class CppcheckMisra(Linter):
    """Provides an interface to cppcheck with MISRA C 2012."""

    cmd = '__cmd__'
    name = 'cppcheck-misra'

    tempfile_suffix = 'c'

    execpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'scripts',
        'cppcheck-misra')

    if sublime.platform() == 'windows' and which('wsl'):
        execpath = util.check_output(['wsl', 'wslpath', execpath]).strip()
        execpath = ['wsl ', execpath]

    defaults = {
        'executable': execpath,
        'selector': 'source.c',
        '--cppcheck-opts': [
            '"--max-configs=1"'
        ],
        '--suppress-rules,': [],
        '--misra-addon': '/usr/local/share/CppCheck/addons/misra.py',
        '--rule-texts': '',
        '--cppcheck-path': '/usr/local/bin'
    }

    regex = OUTPUT_RE
    multiline = False
    error_stream = util.STREAM_STDERR
