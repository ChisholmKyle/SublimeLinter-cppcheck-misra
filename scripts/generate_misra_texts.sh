#!/bin/bash

prog_name=`basename "\${0}"`;

# Usage
usage() {
    echo "Usage: ${prog_name} [ args ]"
    echo "args (optional):"
    echo "    --filename [ pdf filename ]       : default '${MISRAC_FNAME}'"
    echo ""
    echo "Generate MISRA C 2012 texts file from PDF using xPDF for mac or linux."
    echo "xpdf (including pdftotext tool), wget and python3 are required to run the script."
    echo "The generated file 'misra-texts.txt' lists rules with the following structure:"
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

    MISRAC_FNAME=MISRA_C_2012.pdf

    XPDF_TOOLS_PLAT='unknown'
    unamestr=$(uname)
    if [[ "$unamestr" == 'Darwin' ]]; then
       XPDF_TOOLS_PLAT=mac
    elif [[ "$unamestr" == 'Linux' ]]; then
       XPDF_TOOLS_PLAT=linux
    fi

}

#Set defaults
defaults

# Parse arguments
while [[ ${#} -ge 1 && ${1::1} == '-' ]]; do
    key="$1"
    case $key in
        '-h' | '--help' ) usage ;;
        '--filename')
            if [[ ${#} -eq 1 ]] ; then
                usage
            else
                MISRAC_FNAME="$2"
            fi
            shift
            ;;
        * )
            usage
            ;;
    esac
    shift
done

# check platform
if [[ $XPDF_TOOLS_PLAT == 'unknown' ]] ; then
    echo "Unsupported platform (mac or linux not detected)"
  usage
fi

# filename without extension
MISRAC_FNAME_NOEXT="${MISRAC_FNAME%.*}"

# run
pdftotext -enc UTF-8 -eol unix "${MISRAC_FNAME}"
python3 parse_misra_text.py ${MISRAC_FNAME_NOEXT}.txt
