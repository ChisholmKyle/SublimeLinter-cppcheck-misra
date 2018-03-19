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

from SublimeLinter.lint import Linter


class CppcheckMisra(Linter):
    """Provides an interface to cppcheck with MISRA C 2012."""

    regex = r'\[[^:]*:(?P<line>\d+)\] (?P<message>.+)'
    multiline = False

    tempfile_suffix = 'c'

    defaults = {
        'args': [
            '--max-configs=1'
        ],
        'selector': 'source.c',
        'misra_py_addon_file': '/usr/local/share/CppCheck/addons/misra.py',
        'rule_texts_file': ''
    }

    def cmd(self):
        """
        Return the command line to execute.

        We override this method, so we can add extra arguments
        based on the 'rule_texts_file' settings.

        """
        settings = self.get_view_settings()

        result = 'cppcheck-misra'
        result += ' --cppcheck-opts "${args}"'
        result += ' --misra-addon "' + settings.get('misra_py_addon_file') + '"'

        rule_texts_file = settings.get('rule_texts_file', '')
        if rule_texts_file:
            result += ' --rule-texts "' + rule_texts_file + '"'

        result += ' @'

        return result

        # settings = self.get_view_settings()

        # cppcheck_cmd = settings.get('executable', 'cppcheck')
        # cppcheck_cmd += ' ${args} --dump ${file}'

        # python_cmd = 'python "' + settings.get('misra_py_addon_file') + '"'

        # rule_texts_file = settings.get('rule_texts_file', '')
        # if rule_texts_file:
        #     python_cmd += ' --rule-texts=' + rule_texts_file

        # python_cmd += ' ${file}.dump'

        # return ' && '.join([cppcheck_cmd, python_cmd])
