SublimeLinter-contrib-cppcheck-misra
================================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-contrib-cppcheck-misra.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-contrib-cppcheck-misra)

This linter plugin for [SublimeLinter][docs] provides an interface to [cppcheck](cppcheck_homepage) with the development-branch [misra.py addon](cppcheck_addons). It will be used with files that have the “c” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that the development version of `cppcheck` from the GitHub repo is installed on your system. To install `cppcheck`, do the following:

1. Checkout the git repo
   ```
   git checkout https://github.com/danmar/cppcheck
   cd cppcheck
   ```

1. Follow the instructions to build cppcheck. For example, you can install `gcc`, `make` and `cmake` then do the following:
   ```
   mkdir build && cd build
   cmake -G "Unix Makefiles" ..
   make
   ```

1. Install cppcheck and addons (assuming installation director is `/usr/local`). You will likely need to run these command with `sudo`.
   ```
   make install
   cp -rf ../addons /usr/local/share/CppCheck/addons
   cp <package directory>/scripts/cppcheck-misra /usr/local/bin/cppcheck-misra
   chmod +x /usr/local/bin/cppcheck-misra
   ```

### Linter configuration
In order for `cppcheck` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation.

Once you have installed and configured `cppcheck-misra`, you can proceed to install the SublimeLinter-contrib-cppcheck-misra plugin if it is not yet installed.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `cppcheck-misra`. Among the entries you should see `SublimeLinter-contrib-cppcheck-misra`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

In addition to the standard SublimeLinter settings, SublimeLinter-contrib-cppcheck-misra provides its own settings. Those marked as “Inline Setting” or “Inline Override” may also be [used inline][inline-settings].

|Setting|Description|Inline Setting|Inline Override|
|:------|:----------|:------------:|:-------------:|
|misra_texts|(Not yet implemented) A file of descriptions of MISRA rules.|&#10003;| |
|ignore_rules|(Not yet implemented) List of MISRA rules to ignore.|&#10003;| |

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!

[cppcheck_homepage]: https://github.com/danmar/cppcheck
[cppcheck_addons]: https://github.com/danmar/cppcheck/tree/master/addons

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
