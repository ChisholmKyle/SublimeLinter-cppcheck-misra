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
import shlex
from SublimeLinter.lint import Linter, util

OUTPUT_RE = re.compile(r'\[[^:]*:(?P<line>\d+)\] (?P<message>.+)')


class CppcheckMisra(Linter):
    """Provides an interface to cppcheck with MISRA C 2012."""

    name = 'cppcheck-misra'

    tempfile_suffix = 'c'

    defaults = {
        'selector': 'source.c',
        'args': [
            '--max-configs=1'
        ],
        'ignore_rules': [],
        'misra_py_addon': '/usr/local/share/CppCheck/addons/misra.py',
        'rule_texts': ''
    }

    regex = OUTPUT_RE
    multiline = False
    error_stream = util.STREAM_STDERR

    def cmd(self):
        """
        Return the command line to execute.

        We override this method, so we can add extra arguments
        based on the 'rule_texts_file' settings.

        """
        settings = self.get_view_settings()

        result = 'cppcheck-misra --cppcheck-opts "${args}"'
        result += ' --misra-addon ' + shlex.quote(settings.get('misra_py_addon'))

        rule_texts_file = settings.get('rule_texts', '')
        if rule_texts_file:
            result += ' --rule-texts ' + shlex.quote(rule_texts_file)

        ignore_rules = settings.get('ignore_rules', [])
        if ignore_rules:
            result += ' --ignore-rules ' + shlex.quote(','.join(ignore_rules))

        result += ' ${temp_file}'

        return result
