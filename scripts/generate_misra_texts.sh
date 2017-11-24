#!/bin/bash

prog_name=`basename "\${0}"`;

# Usage
usage() {
    echo "Usage: ${prog_name} [ args ]"
    echo "args (optional):"
    echo "    --filename [ pdf filename ]       : default '${MISRAC_FNAME}'"
    echo "    --start [ Appendix A page start ] : default '${MISRAC_APPENDIXA_PAGE_START}'"
    echo "    --end [ Appendix A page end ]     : default '${MISRAC_APPENDIXA_PAGE_END}'"
    echo "    --xpdf-version [ xPDF version ]   : default '${XPDF_TOOLS_VERSION}'"
    echo ""
    echo "Generate MISRA C 2012 texts file from PDF using xPDF for mac or linux."
    echo "wget and python3 are required to run the script."
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
    MISRAC_APPENDIXA_PAGE_START=188
    MISRAC_APPENDIXA_PAGE_END=196
    XPDF_TOOLS_VERSION=4.00

    XPDF_TOOLS_PLAT='unknown'
    unamestr=$(uname)
    if [[ "$unamestr" == 'Darwin' ]]; then
       XPDF_TOOLS_PLAT=mac
    elif [[ "$unamestr" == 'Linux' ]]; then
       XPDF_TOOLS_PLAT=linux
    fi

    XPDF_TOOLS_MACHINE=32
    unamestr=$(uname -m)
    if [[ "$unamestr" == 'x86_64' ]]; then
       XPDF_TOOLS_MACHINE=64
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
        '--start')
            if [[ ${#} -eq 1 ]] ; then
                usage
            else
                MISRAC_APPENDIXA_PAGE_START="$2"
            fi
            shift
            ;;
        '--end')
            if [[ ${#} -eq 1 ]] ; then
                usage
            else
                MISRAC_APPENDIXA_PAGE_END="$2"
            fi
            shift
            ;;
        '--xpdf-version')
            if [[ ${#} -eq 1 ]] ; then
                usage
            else
                XPDF_TOOLS_VERSION="$2"
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
# xPDF filename
XPDF_TOOLS_NAME=xpdf-tools-${XPDF_TOOLS_PLAT}-${XPDF_TOOLS_VERSION}

# download
if [[ ! -f "${XPDF_TOOLS_NAME}/bin${XPDF_TOOLS_MACHINE}/pdftotext" ]]; then
    wget http://www.xpdfreader.com/dl/${XPDF_TOOLS_NAME}.tar.gz
    tar xvzf ${XPDF_TOOLS_NAME}.tar.gz
fi

# run
./${XPDF_TOOLS_NAME}/bin${XPDF_TOOLS_MACHINE}/pdftotext -simple -f ${MISRAC_APPENDIXA_PAGE_START} -l ${MISRAC_APPENDIXA_PAGE_END} "${MISRAC_FNAME}"
python3 parse_misra_text.py ${MISRAC_FNAME_NOEXT}.txt
