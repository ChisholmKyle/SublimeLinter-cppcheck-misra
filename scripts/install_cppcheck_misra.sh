#!/bin/bash

prog_name=$(basename "${0}")
this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Usage
usage() {
    echo "Usage: ${prog_name} [ args ]"
    echo "args (optional):"
    echo "    --prefix [ install prefix ]  : default '${PREFIX}'"
    echo "    --skip-build                 : skip dev build of Cppcheck from source"
    echo ""
    echo "Build and install cppcheck with misra.py addon"
    echo "from master branch of https://github.com/danmar/cppcheck."
    echo "Compiling cppcheck requires git, cmake, gcc/clang, and make."
    echo ""
    echo "Helper scripts 'cppcheck-misra' and 'cppcheck-misra-gentexts' are installed to simplify processing."
    echo "Run 'cppcheck-misra -h' and 'cppcheck-misra-gentexts -h' for more information."
    exit 1
}

# Defaults
defaults() {

    PREFIX=/usr/local
    skip_build=0

}

# Set defaults
defaults

# Parse arguments
while [[ ${#} -ge 1 && ${1::1} == '-' ]]; do
    key="$1"
    case $key in
        '-h' | '--help' ) usage ;;
        '--prefix')
            if [[ ${#} -eq 1 ]] ; then
                usage
            else
                PREFIX="$2"
            fi
            shift
            ;;
        '--skip-build' )
            skip_build=1
            ;;
        * )
            usage
            ;;
    esac
    shift
done

if [ "$skip_build" -eq 0 ] ; then
    # Build cppcheck
    echo "Installing development build of ccpcheck at prefix=${PREFIX}"
    git clone https://github.com/danmar/cppcheck
    cd cppcheck

    mkdir build && cd build
    cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ..
    PREFIX=${PREFIX} make
    sudo make install
    sudo cp -rf ../addons "${PREFIX}/share/CppCheck/addons"
fi


cat <<EOF > "${this_dir}/cppcheck-misra"
#!/bin/bash

prog_name=$(basename "\${0}")

# Usage
usage() {
    echo "Usage: \${prog_name} [ args ] [ source files ]"
    echo "args (optional):"
    echo "    --version                               : output cppcheck version"
    echo "    --rule-texts [ rule texts file ]        : default '\${RULE_TEXTS}'"
    echo "    --cppcheck-opts [ cppcheck options ]    : pass options to cppcheck"
    echo ""
    echo "MISRA C 2012 checks on source files using cppcheck and misra.py addon."
    echo "Optionally specify plain text file with rule descriptions. The text file"
    echo "should list rules with the following structure:"
    echo ""
    echo "Rule <topic number>.<rule number>"
    echo "    <category>"
    echo "    <text>"
    echo ""
    echo "Rule <topic number>.<rule number>"
    echo "    <category>"
    echo "    <text>"
    echo ""
    echo "..."
    echo ""
    echo "where <topic number> and <rule number> are integers,"
    echo "<category> is 'Mandatory', 'Required', or 'Advisory',"
    echo "and <text> is the rule description."
    exit 1
}

# defaults
defaults() {
    RULE_TEXTS=''
    CPP_OPTS=''
}

#Set defaults
defaults

# Parse arguments
while [[ \${#} -ge 1 && \${1::1} == '-' ]]; do
    key="\$1"
    case \$key in
        '-h' | '--help' ) usage ;;
        '--version' )
            cppcheck --version
            exit
            ;;
        '--rule-texts')
            if [[ \${#} -eq 1 ]] ; then
                usage
            else
                RULE_TEXTS="\$2"
            fi
            shift
            ;;
        '--cppcheck-opts')
            if [[ \${#} -eq 1 ]] ; then
                usage
            else
                CPP_OPTS="\$2"
            fi
            shift
            ;;
        * )
            usage
            ;;
    esac
    shift
done

if [[ -z "\${RULE_TEXTS}" ]] ; then
for f in "\$@" ; do
    cppcheck \${CPP_OPTS} --dump "\$f" && python ${PREFIX}/share/CppCheck/addons/misra.py "\$f.dump"
done
else
for f in "\$@" ; do
    cppcheck \${CPP_OPTS} --dump "\$f" && python ${PREFIX}/share/CppCheck/addons/misra.py --rule-texts="\${RULE_TEXTS}" "\$f.dump"
done
fi

EOF

# install cppcheck-misra script for linter
sudo cp -f "${this_dir}/cppcheck-misra" "${PREFIX}/bin/cppcheck-misra"
sudo chmod +x "${PREFIX}/bin/cppcheck-misra"
echo "Installed '${PREFIX}/bin/cppcheck-misra'"

# install cppcheck-misra-gentexts script for linter
sudo cp -f "${this_dir}/cppcheck-misra-gentexts" "${PREFIX}/bin/cppcheck-misra-gentexts"
sudo chmod +x "${PREFIX}/bin/cppcheck-misra-gentexts"
sudo cp -f "${this_dir}/cppcheck-misra-parsetexts.py" "${PREFIX}/bin/cppcheck-misra-parsetexts.py"
sudo chmod +x "${PREFIX}/bin/cppcheck-misra-parsetexts.py"
echo "Installed '${PREFIX}/bin/cppcheck-misra-gentexts' and helper python script '${PREFIX}/bin/cppcheck-misra-parsetexts.py'"

