SublimeLinter-contrib-cppcheck-misra
================================

[![Build Status](https://travis-ci.org/ChisholmKyle/SublimeLinter-contrib-cppcheck-misra.svg?branch=master)](https://travis-ci.org/ChisholmKyle/SublimeLinter-contrib-cppcheck-misra)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [cppcheck](https://github.com/danmar/cppcheck) with the development-branch [misra.py addon](https://github.com/danmar/cppcheck/tree/master/addons). It will be used with files that have the “c” syntax.

## Installation

SublimeLinter must be installed in order to use this plugin.

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

### Install `cppcheck` with `misra.py` addon

Before using this plugin, you must have a version of `cppcheck` which also includes the [misra.py addon](https://github.com/danmar/cppcheck/tree/master/addons).

You may want to build and install the latest development branch of cppcheck with misra.py by running the bash script [`scripts/install_cppcheck.sh`](scripts/install_cppcheck.sh). Run `install_cppcheck.sh -h` for more information on the script.

If you already have cppcheck installed, try the latest misra.py file with:
```sh
    wget https://raw.githubusercontent.com/danmar/cppcheck/master/addons/misra.py
    sudo mkdir -p /usr/local/share/CppCheck/addons
    sudo cp -f misra.py /usr/local/share/CppCheck/addons/misra.py
```

### Install `cppcheck-misra` script

The script [`scripts/cppcheck-misra`](scripts/cppcheck-misra) is required for the linter to work. Run `cppcheck-misra -h` for more information on the script. To install, simply copy and make executable somewhere on your PATH. For example:
```sh
    sudo cp -f scripts/cppcheck-misra /usr/local/bin/cppcheck-misra
    sudo chmod +x /usr/local/bin/cppcheck-misra
```

### Generate texts from MISRA C:2012 guidelines

Due to MISRA rules, only rule check numbers are allowed in free and open source software so you need to supply your own set of texts for each rule. If you have a pdf of MISRA C:2012 guidelines, the Python 3.x script [`scripts/cppcheck-misra-parsetexts.py`](scripts/cppcheck-misra-parsetexts.py) generates the rules text file from Appendix A (Summary of guidelines).

Generate rules text:
```sh
    python3 scripts/cppcheck-misra-parsetexts.py /path/to/MISRA_C_2012.pdf
```

Now 'MISRA_C_2012_Rules.txt' should be in the '/path/to/' directory

### Make sure your settings reflect installed file locations

In your project settings, set

```json
"settings": {
    "SublimeLinter.linters.cppcheck-misra.misra_py_addon": "/usr/local/share/CppCheck/addons/misra.py",
    "SublimeLinter.linters.cppcheck-misra.rule_texts": "/path/to/MISRA_C_2012_Rules.txt"
}
```

### Configure PATH

In order for `cppcheck-misra` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings
- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

Note that the "args" setting passes arguments to `cppcheck`. You may get many duplicates for each detected configuration with cppcheck. To remedy this, try passing the argument "--max-configs=1" (See [`man cppcheck`](https://linux.die.net/man/1/cppcheck)).

Additional SublimeLinter-contrib-cppcheck-misra settings:

|Setting|Description|
|:------|:----------|
|misra_py_addon|(Required) The misra.py addon file|
|rule_texts|(Recommended) A file of descriptions of MISRA rules|
|suppress_rules|(Optional) List of rules to ignore|

In project-specific settings, note that SublimeLinter allows [expansion variables](http://sublimelinter.readthedocs.io/en/latest/settings.html#settings-expansion). For example, the variable '${project_path}' can be used to specify a path relative to the project folder. Example settings:

```json
"settings": {
    "SublimeLinter.linters.cppcheck-misra.misra_py_addon": "/usr/local/share/CppCheck/addons/misra.py",
    "SublimeLinter.linters.cppcheck-misra.rule_texts": "${project_path}/misra/MISRA_C_2012_Rules.txt",
    "SublimeLinter.linters.cppcheck-misra.ignore_rules": [
        "8.14",
        "12.1"
    ],
    "SublimeLinter.linters.cppcheck-misra.args": [
        "--max-configs=1"
    ]
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
