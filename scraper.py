#!/usr/bin/python3 -Es
import argparse
import os
import re
from bs4 import BeautifulSoup

__author__ = 'Stefan Weiberg'
__license__ = 'EUPLv2'
__version__ = '0.0.1'
__maintainer__ = 'Stefan Weiberg'
__email__ = 'stefan.weiberg@hetzner.com'
__status__ = 'Development'

desc = "Script to create a Mermaid visualisation of an OpenProject workflow page"
parser = argparse.ArgumentParser()

parser.add_argument("-f", dest="file", type=str, required=True,
                    help="HTML file of the workflow page")

args = parser.parse_args()
file = args.file

with open(file) as html:
    soup = BeautifulSoup(html.read(), "html.parser")
    always = soup.find("div", {"id": "workflow_form_always"})
    rows = always.find_all("tr", class_="-table-border-left")

def get_status_text():
    status_dict = dict()
    for row in rows:
        status_raw = row.find("td", class_="workflow-table--current-status -table-border-right")
        status_text = re.sub(r'Alle in Zeile an\/abwählen',r'',status_raw.text.strip()).strip()
        status_id = re.findall(r'(status_)(.*)(_[0-9]*_)', row.input['id'])[0][1]
        status_dict[status_id] = status_text
    return status_dict

def get_workflow():
    workflow = []
    for row in rows:
        input_fields = row.find_all('input')
        for input_field in input_fields:
            regex_groups = re.findall(r'(status_)([0-9]*)(_)([0-9]*)(_)', input_field['id'])
            old_status = regex_groups[0][1]
            new_status = regex_groups[0][3]
            if old_status == new_status:
                continue
            workflow.append(old_status + ' --> ' + new_status)
    return workflow

def build_mermaid(status,workflow):
    print('```mermaid')
    print('stateDiagram-v2')
    for key, value in status.items():
        print('    ' + key + ': ' + value)
    for line in workflow:
        print('    ' + line)
    print('```')

if __name__ == "__main__":
    try:
        status = get_status_text()
        workflow = get_workflow()
        build_mermaid(status,workflow)
    except Exception as error:
        print('ERROR', error)
    pass
