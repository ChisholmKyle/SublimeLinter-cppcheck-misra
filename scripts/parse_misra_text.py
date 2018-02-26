"""Extract MISRA-C 2012 rules."""
import re
import sys
import json

# rules
_appendixa_regex = re.compile(r'Appendix A Summary of guidelines\n')
_appendixb_regex = re.compile(r'Appendix B Guideline attributes\n')
_rule_regex = re.compile(r'(Rule|Dir) (\d+)\.(\d+)\n\n(Advisory|Required|Mandatory)\n\n([^\n]+)\n')
_line_regex = re.compile(r'([^\n]+)\n')

def misra_dict_to_text(misra_dict):
    """Convert dict to string readable by cppcheck's misra.py addon."""
    misra_str = ''
    for num1 in misra_dict:
        for num2 in misra_dict[num1]:
            misra_str += '\n{} {}.{}\n'.format(misra_dict[num1][num2]['type'], num1, num2)
            misra_str += '    {}\n'.format(misra_dict[num1][num2]['category'])
            misra_str += '    {}\n'.format(misra_dict[num1][num2]['text'])
    return misra_str


def parse_misra_xpdf_output(misra_file):
    """Initialize mass properties from a file."""
    misra_dict = {}

    fp = open(misra_file, 'r', encoding="utf-8")
    fp_text = fp.read()
    fp.close()

    # end of appendix A
    appb_end_res = _appendixb_regex.search(fp_text)
    last_index = appb_end_res.regs[0][0]

    appres = _appendixa_regex.search(fp_text)
    if appres:
        start_index = appres.regs[0][1]
        res = _rule_regex.search(fp_text, start_index)
        while res:
            start_index = res.regs[0][1]
            ruletype = res.group(1)
            rulenum1 = res.group(2)
            rulenum2 = res.group(3)
            category = res.group(4)
            ruletext = res.group(5).strip()
            statereadingrule = True
            while statereadingrule:
                lineres = _line_regex.match(fp_text, start_index)
                if lineres:
                    start_index = lineres.regs[0][1]
                    stripped_line = lineres.group(1).strip()
                    ruletext += ' ' + stripped_line
                else:
                    # empty line, stop reading text and save to dict
                    if rulenum1 not in misra_dict:
                        misra_dict[rulenum1] = {}
                    misra_dict[rulenum1][rulenum2] = {
                        'type': ruletype,
                        'category': category,
                        'text': ruletext
                    }
                    statereadingrule = False
            res = _rule_regex.search(fp_text, start_index)
            if res and (last_index < res.regs[0][0]):
                break
    fp.close()

    return misra_dict


misra_dict = parse_misra_xpdf_output(sys.argv[1])
misra_text = misra_dict_to_text(misra_dict)

obj = open('rule-texts.json', 'w', encoding='utf-8')
obj.write(json.dumps(misra_dict, indent=4))
obj.close()

obj = open('rule-texts.txt', 'w', encoding='utf-8')
obj.write(misra_text)
obj.close()

print('Output rule-texts.txt and rule-texts.json')
