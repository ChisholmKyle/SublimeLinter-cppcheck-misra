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

from SublimeLinter.lint import Linter, util
import sublime
import os
import string


def get_project_folder():
    """Return the project folder path."""
    proj_file = sublime.active_window().project_file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    # Use current file's folder when no project file is opened.
    proj_file = sublime.active_window().active_view().file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    return '.'


def apply_template(s):
    """Replace "project_folder" string with the project folder path."""
    mapping = {
        "project_folder": get_project_folder()
    }
    templ = string.Template(s)
    return templ.safe_substitute(mapping)


class CppcheckMisra(Linter):
    """Provides an interface to cppcheck with MISRA C 2012."""

    syntax = ('c')
    executable = 'cppcheck-misra'

    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+) '
    version_requirement = '>= 1.80'

    regex = r'\[[^:]*:(?P<line>\d+)\] (?P<message>.+)'

    multiline = False
    line_col_base = (1, 1)
    tempfile_suffix = 'c'
    error_stream = util.STREAM_BOTH
    selectors = {}
    word_re = None

    inline_settings = None
    inline_overrides = None
    comment_re = None

    defaults = {
        'rule_texts_file': '',
        'cppcheck_max_configs': 1,
        'ignore_rules': []
    }

    def cmd(self):
        """
        Return the command line to execute.

        We override this method, so we can add extra arguments
        based on the 'rule_texts_file' settings.

        """
        result = 'cppcheck-misra'
        settings = self.get_view_settings()

        # load custom settings
        cppcheck_max_configs = settings.get('cppcheck_max_configs', 1)

        cppcheck_opts = ''
        if cppcheck_max_configs:
            cppcheck_opts += ' --max-configs=' + str(cppcheck_max_configs)

        if cppcheck_opts:
            result += ' --cppcheck-opts "' + cppcheck_opts.replace('"', '\\"') + '"'

        rule_texts_file = settings.get('rule_texts_file', '')
        if rule_texts_file:
            result += ' --rule-texts "' + apply_template(rule_texts_file) + '"'

        return result + ' @'
