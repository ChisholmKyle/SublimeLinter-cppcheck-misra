SublimeLinter-contrib-cppcheck-misra
================================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-contrib-cppcheck-misra.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-contrib-cppcheck-misra)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [cppcheck](https://github.com/danmar/cppcheck) with the development-branch [misra.py addon](https://github.com/danmar/cppcheck/tree/master/addons). It will be used with files that have the “c” syntax.

## Installation

SublimeLinter must be installed in order to use this plugin.

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

### Install `cppcheck` With `misra.py` Addon as `cppcheck-misra`

Before using this plugin, you must ensure that the development version of `cppcheck` from the GitHub repo (master branch) is installed on your system with the misra.py addon. If you have Linux or Mac, this process is simplified by running the bash script [`scripts/install_cppcheck_misra.sh`](scripts/install_cppcheck_misra.sh). This installs the [`cppcheck-misra`](scripts/cppcheck-misra) script which simplifies the MISRA rules check and is required for this linter to work. Run `install_cppcheck_misra.sh -h` for more information on the install script and `cppcheck-misra -h` after installation for details.

Due to MISRA rules, only rule check numbers are allowed in FLOSS so you need to supply your own set of texts for each rule. If you have a pdf of MISRA C:2012 guidelines, the [`cppcheck-misra-gentexts`](scripts/cppcheck-misra-gentexts) script generates the rules text file from Appendix A (Summary of guidelines). Run `cppcheck-misra-gentexts -h` for more information on running the script and the format of the rules texts.

An example installation process:
   ```sh
   cd scripts
   ./install_cppcheck_misra.sh --prefix=/usr/local
   cppcheck-misra-gentexts --filename /path/to/MISRA_C_2012.pdf
   # now 'rule-texts.txt' should be in the '/path/to/' directory
   ```

Try running `cppcheck-misra` on a source file:
   ```sh
   cppcheck-misra --rule-text /path/to/rule-texts.txt source_file.c
   ```

### Configure PATH

In order for `cppcheck-misra` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings
- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

Additional SublimeLinter-contrib-cppcheck-misra settings:

|Setting|Description|
|:------|:----------|
|rule_texts_file|A file of descriptions of MISRA rules.|
|cppcheck_max_configs|Value for cppcheck --max-configs option. See [`man cppcheck`](https://linux.die.net/man/1/cppcheck).|
|ignore_rules|(Not yet implemented) List of MISRA rules to ignore.|


In project-specific settings, note that SublimeLinter allows [expansion variables](http://sublimelinter.readthedocs.io/en/latest/settings.html#settings-expansion). For example the variable '${project_path}' can be used to specify a path relative to the project folder. For example:

```
"SublimeLinter":
{
    "linters":
    {
        "cppcheckmisra": {
            "rule_texts_file": "${project_path}/misra/rule-texts.txt",
            "cppcheck_max_configs": 1
        }
    }
}
```

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
