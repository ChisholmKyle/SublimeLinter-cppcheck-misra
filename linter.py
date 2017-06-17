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


class CppcheckMisra(Linter):
    """Provides an interface to cppcheck with MISRA C 2012."""

    syntax = ('c')

    executable = 'cppcheck'
    cmd = 'cppcheck-misra @'
    # cmd = 'cppcheck --dump @ && python /path/to/misra.py @.dump'

    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+) '
    version_requirement = '>= 1.80'

    regex = r'\[[^:]*:(?P<line>\d+)\] (?P<message>[^(]+)\('
    multiline = False
    error_stream = util.STREAM_BOTH

    tempfile_suffix = 'c'

    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None
