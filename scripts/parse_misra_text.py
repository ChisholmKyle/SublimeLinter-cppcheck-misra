"""Extract MISRA-C 2012 rules."""
import re
import sys
import json

# rules
_rule_regex = re.compile(r'^\s*Rule (\d+)\.(\d+)' +
                         r'\s*(Advisory|Required|Mandatory)' +
                         r'(.*)$')

# regex to remove page numbers mixed up in rule texts
_pgnum_regex = re.compile(r'\s*\d\d\d\s*')


def misra_dict_to_text(misra_dict):
    """Convert dict to string readable by cppcheck's misra.py addon."""
    misra_str = ''
    for num1 in misra_dict:
        for num2 in misra_dict[num1]:
            misra_str += '\nRule {}.{}\n'.format(num1, num2)
            misra_str += '    {}\n'.format(misra_dict[num1][num2]['category'])
            misra_str += '    {}\n'.format(misra_dict[num1][num2]['text'])
    return misra_str


def parse_misra_xpdf_output(misra_file):
    """Initialize mass properties from a file."""
    misra_dict = {}

    rulenum1 = '0'
    rulenum2 = '0'
    category = ''
    ruletext = ''

    statereadingtext = False

    fp = open(misra_file)
    for i, line in enumerate(fp):
        if not statereadingtext:
            res = _rule_regex.match(line)
            if res:
                rulenum1 = res.group(1)
                rulenum2 = res.group(2)
                category = res.group(3)
                ruletext = res.group(4).strip()
                statereadingtext = True
        else:
            stripped_line = line.strip()
            if not stripped_line:
                # empty line, stop reading text and save to dict
                if rulenum1 not in misra_dict:
                    misra_dict[rulenum1] = {}
                misra_dict[rulenum1][rulenum2] = {
                    'category': category,
                    'text': _pgnum_regex.sub(' ', ruletext).strip()
                }
                statereadingtext = False
            else:
                ruletext += ' ' + stripped_line
    fp.close()

    return misra_dict


misra_dict = parse_misra_xpdf_output(sys.argv[1])
misra_text = misra_dict_to_text(misra_dict)

obj = open('rule-texts.json', 'w')
obj.write(json.dumps(misra_dict, indent=4))
obj.close

obj = open('rule-texts.txt', 'w')
obj.write(misra_text)
obj.close

print('Output rule-texts.txt and rule-texts.json')
