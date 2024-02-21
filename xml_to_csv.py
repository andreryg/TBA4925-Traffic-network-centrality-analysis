import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

def read_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return tree, root

def process_element_tolist(element):
    def process_element(element):

        #print(f"Element: {element.tag}, Attributes: {element.attrib}, Text: {element.text}")
        nonlocal element_list
        if "tettstednummer" in element.tag or "tettstednavn" in element.tag or "totalBefolkning" in element.tag or "posList" in element.tag:
            element_list.append(element.text)

        for child in element:
            process_element(child)

    element_list = []
    process_element(element)
    return element_list
    

def xml_to_pandas(file):
    tree, root = read_xml(file)
    elements_list = []
    for element in root:
        if "boundedBy" not in element.tag:
            element_list = process_element_tolist(element)
            posList_list = element_list[:-3]
            element_list = element_list[-3:]
            for posList in posList_list:
                elements_list.append(dict((v,[*element_list, posList][i]) for i,v in enumerate(['tettstednummer', 'tettstednavn', 'totalBefolkning', 'posList'])))
    elements = pd.DataFrame(elements_list, columns=['tettstednummer', 'tettstednavn', 'totalBefolkning', 'posList'])
    print(elements.size)

    return elements

def read_csv(file):
    dataframe = pd.read_csv(file)
    return dataframe

#print(read_csv("stemmekrets_csv.csv"))

pd = xml_to_pandas("tettsteder.gml")

pd.to_csv("tettsteder_xml_file.csv", encoding='utf-8', index=False)