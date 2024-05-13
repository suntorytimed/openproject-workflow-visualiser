#!/usr/bin/python3 -Es
'''
Script to create a Mermaid visualisation of an OpenProject workflow page
'''
import argparse
import os
import re
import subprocess
import tempfile
from bs4 import BeautifulSoup

__author__ = 'Stefan Weiberg'
__license__ = 'EUPLv2'
__version__ = '0.0.1'
__maintainer__ = 'Stefan Weiberg'
__email__ = 'stefan.weiberg@hetzner.com'
__status__ = 'Development'

parser = argparse.ArgumentParser()

parser.add_argument("-f", dest="file", type=str, required=True,
                    help="HTML file of the workflow page")
parser.add_argument("-o", dest="output", type=str,
                    help="output file for PNG rendering with mermaid-cli (mmdc in $PATH)")

args = parser.parse_args()
file = args.file
output = args.output

with open(file, encoding="utf8") as html:
    soup = BeautifulSoup(html.read(), "html.parser")
    always = soup.find("div", {"id": "workflow_form_always"})
    rows = always.find_all("tr", class_="-table-border-left")

def get_status_text():
    '''
    Extracts a key value pair for each status mentioned in the HTML. As each status does have a
    unique ID and each row in a table contains a status, the text can be extracted from the row
    and get paired with the old status ID mentioned in the checkbox ID in one of the checkboxes
    of the row.
    
    :return: dictionary with status ID as key and status text as value
    '''
    status_dict = {}
    for row in rows:
        status_raw = row.find("td", class_="workflow-table--current-status -table-border-right")
        status_text = re.sub(r'Alle in Zeile an\/abwählen',r'',status_raw.text.strip()).strip()
        status_id = re.findall(r'(status_)(.*)(_[0-9]*_)', row.input['id'])[0][1]
        status_dict[status_id] = status_text
    return status_dict

def get_workflow():
    '''
    Creates Mermaid formatted lines for each status change in the workflow. Uses the old and new
    status information which is part of the ID string of each checkbox.
    
    :return: list of Mermaid formatted strings for each status change in the workflow
    '''
    workflow_list = []
    for row in rows:
        input_fields = row.find_all('input')
        for input_field in input_fields:
            # ensure that only checked checkboxes are used
            try:
                input_field['checked']
            except KeyError:
                continue
            regex_groups = re.findall(r'(status_)([0-9]*)(_)([0-9]*)(_)', input_field['id'])
            old_status = regex_groups[0][1]
            new_status = regex_groups[0][3]
            if old_status == new_status:
                continue
            workflow_list.append(old_status + ' --> ' + new_status)
    return workflow_list

def print_mermaid(status_dict,workflow_list):
    '''
    Prints out a Mermaid state diagram for the workflow.
    '''
    print('```mermaid')
    print('stateDiagram-v2')
    for key, value in status_dict.items():
        print('    ' + key + ': ' + value)
    for line in workflow_list:
        print('    ' + line)
    print('```')

def generate_svg(status_dict,workflow_list,output):
    '''
    Output a PNG rendering of the workflow with mermaid-cli (requires mmdc in $PATH).
    '''
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
        tmp.write('stateDiagram-v2\n')
        for key, value in status_dict.items():
            tmp.write(f'    {key}: {value}\n')
        for line in workflow_list:
            tmp.write(f'    {line}\n')
    try:
        subprocess.run(["mmdc", "-i", tmp.name, "-e", "png", "-o", output], check=True)
    finally:
        tmp.close()
        os.remove(tmp.name)
    
if __name__ == "__main__":
    status = get_status_text()
    workflow = get_workflow()
    if output is not None:
        generate_svg(status,workflow,output)
    else:
        print_mermaid(status,workflow)
