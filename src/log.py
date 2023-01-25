import heapq
import os
import datetime
import binascii
import json
import xml.etree.ElementTree as ET
import re

#xml
def log_to_xml(config, input_file, output_file, result):
    """
    Loguje informace o spuštění programu do souboru ve formátu XML.

    :param:
    config (str): Konfigurace programu.
    operation (str): Co program zpracoval.
    result (str): Výsledek zpracování (úspěch/chyba).

    :return:
    None
    """

    root = ET.Element("log")

    config_elem = ET.SubElement(root, "config")
    config_elem.text = config

    now = datetime.datetime.now()
    date_time_elem = ET.SubElement(root, "date_time")
    date_time_elem.text = now.strftime("%Y-%m-%d %H:%M:%S")

    operation_elem = ET.SubElement(root, "input_file")
    operation_elem.text = input_file

    operation_elem = ET.SubElement(root, "output_file")
    operation_elem.text = output_file

    result_elem = ET.SubElement(root, "result")
    result_elem.text = result

    tree = ET.ElementTree(root)

    if not os.path.exists("../logs/log.xml"):
        print("Byl vytvoren log.xml soubor umisteny ve slozce /logs/")
        print("Log byl zapsan")
        f = open("../logs/log.xml", "w")
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<root>\n')
        f.write(ET.tostring(root).decode("utf-8"))
        f.write('\n</root>')
        f.close()
    else:
        # Open the XML file in read mode
        with open("../logs/log.xml", "r") as f:
            # Read the entire file into memory
            lines = f.readlines()

        # Remove the last line
        lines = lines[:-1]

        # Open the XML file in write mode
        with open("../logs/log.xml", "w") as f:
            # Write the lines back to the file
            f.writelines(lines)

        print("Log byl zapsan")
        f = open("../logs/log.xml", "a")
        f.write("\n" + ET.tostring(root).decode("utf-8"))
        f.write('\n</root>')
        f.close()

    #with open("log.xml", "a", encoding="utf-8") as f:
    #       f.write("\n"+ET.tostring(root).decode("utf-8"))


def parse_xml(file_path):

    tree = ET.parse(file_path)
    root = tree.getroot()

    logs = []

    for log in root:
        log_dict = {}
        for element in log:
            log_dict[element.tag] = element.text
        logs.append(log_dict)

    return logs

if __name__ == "__main__":
    pass
