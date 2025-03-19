import os
os.environ["OMP_NUM_THREADS"] = "1"
import pandas as pd
import xmlschema
import re
import xml.etree.ElementTree as ET
from lxml import etree
import pickle

def process_excel(file, sheet_name: str = 'Database (Columns)') -> pd.DataFrame:
    df = pd.read_excel(file, sheet_name=sheet_name, header=[0,1,2,3,4,5,6,7,8])
    columns_to_drop = [col for col in df.columns if 'E' in col]
    df = df.drop(columns=columns_to_drop)
    df = df[df.iloc[:, 0].notna()]
    df = df.drop(index=1, errors='ignore')
    return df

def load_dict():
    file_path = os.path.join(os.path.dirname(__file__), 'AM_excel_mapping.pkl')
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data

def load_test_schemas():
    script_dir = os.path.dirname(__file__)
    Tests = {
        "RuttingTestResults": "RuttingExp",
        "MarshallTestResults": "MarshallExp",
        "ITSTestResults": "ITSExp",
        "TSRSTestResults": "TSRSTExp",
        "UTSTestResults": "UTSTExp",
        "StiffnessTestResults": "StiffnessExp"
    }
    Schemas = {
        "RuttingExp": xmlschema.XMLSchema(os.path.join(script_dir, 'AsphaltDB-Rutting.xsd')),
        "MarshallExp": xmlschema.XMLSchema(os.path.join(script_dir, 'AsphaltDB-Marshall.xsd')),
        "ITSExp": xmlschema.XMLSchema(os.path.join(script_dir, 'AsphaltDB-ITS.xsd')),
        "TSRSTExp": xmlschema.XMLSchema(os.path.join(script_dir, 'AsphaltDB-TSRST.xsd')),
        "UTSTExp": xmlschema.XMLSchema(os.path.join(script_dir, 'AsphaltDB-UTST.xsd')),
        "StiffnessExp": xmlschema.XMLSchema(os.path.join(script_dir, 'AsphaltDB-Stiffness.xsd'))
    }
    return Tests, Schemas
    
def xml_creator(row, col_to_paths, root_name):
    root = ET.Element(root_name)
    for column, paths in col_to_paths.items():
        if column not in row:
            print(f"Warning: Column '{column}' not found in DataFrame row.")
            continue
        column_value = row[column]
        if pd.isna(column_value) or column_value == '':
            continue
        if isinstance(column_value, float) and column_value.is_integer():
            column_value = int(column_value)
        if isinstance(column_value, pd.Timestamp):
            column_value = column_value.strftime("%Y-%m-%d")
        for path in paths:
            path_parts = path.split('.')
            parent = root
            for part in path_parts:
                child = next((elem for elem in parent if elem.tag == part), None)
                if child is None:
                    child = ET.SubElement(parent, part)
                parent = child
            child.text = str(column_value)
    return ET.tostring(root, encoding="unicode")

def remove_nmbrd_tags(xml_string):
    root = ET.fromstring(xml_string)
    for elem in root.iter():
        new_tag = elem.tag.split('_')[0]
        elem.tag = new_tag
    return ET.tostring(root, encoding="unicode")

def seperate_semicolons(xml_s, elements):
    for ele in elements:
        pattern = rf'(<{ele}.*?>)(.*?)(</{ele}>)'
        matches = re.findall(pattern, xml_s, re.DOTALL)
        for match in matches:
            opening, content, closing = match
            child_ele = re.findall(r'<(.*?)>(.*?)</\1>', content)
            split_val = {child[0]: child[1].split(';') for child in child_ele if ';' in child[1]}
            num_ele = max(len(values) for values in split_val.values())
            new_eles = []
            for i in range(num_ele):
                new_ele = f'<{ele}>'
                for tag, values in split_val.items():
                    new_ele += f'<{tag}>{values[i].strip()}</{tag}>'
                new_ele += f'</{ele}>'
                new_eles.append(new_ele)
            xml_s = xml_s.replace(f'{opening}{content}{closing}', ''.join(new_eles), 1)
    return xml_s

def keep_only_first_child(xml_string, parent_tags):
    root = ET.fromstring(xml_string)  
    for parent_tag in parent_tags:
        for parent in root.findall(f".//{parent_tag}"):
            children = list(parent)
            if len(children) > 1:
                first_child = children[0]
                parent.clear()
                parent.append(first_child)
    return ET.tostring(root, encoding="unicode")

def extract_single_xmls(Record, Tests):
    extracted_xmls = []    
    datasourcenode = re.search(r'<DataSource>(.*?)</DataSource>', Record, re.DOTALL)
    mixturenode = re.search(r'<Mixture>(.*?)</Mixture>', Record, re.DOTALL)
    datasource = datasourcenode.group(0) if datasourcenode else ''
    mixture = mixturenode.group(0) if mixturenode else ''
    for node, new_root in Tests.items():
        pattern = fr'<({node})>(.*?)</\1>'
        matches = re.finditer(pattern, Record, re.DOTALL)        
        for match in matches:
            results = match.group(0)            
            notesnode = re.search(r'<Notes>(.*?)</Notes>', Record[match.end():], re.DOTALL)
            notes = notesnode.group(0) if notesnode else ''
            new_xml = f'<{new_root}>{datasource}{mixture}{results}{notes}</{new_root}>'      
            extracted_xmls.append(new_xml)
    return extracted_xmls

def add_names(nested_list):
    file_dict = {}  
    for i, sublist in enumerate(nested_list):
        if isinstance(sublist, list):
            for j, item in enumerate(sublist):
                root = etree.XML(item).tag
                file_name = f"Row {i+1} - {root.rstrip('Exp')}"
                file_dict[file_name] = item  
        else:
            root = etree.XML(sublist).tag
            file_name = f"Row {i} - {root.rstrip('Exp')}"
            file_dict[file_name] = sublist  
    return file_dict 
    
def process_xml_final(excel):
    df = process_excel(excel)
    dic=load_dict()
    Tests, Schemas = load_test_schemas()
    xml_0 = [xml_creator(row, dic, "AsphaltMine") for _, row in df.iterrows()]
    xml_1 = [remove_nmbrd_tags(xml) for xml in xml_0]
    semicolons = ["Point", "AdditionalProperties", "OtherMixingProperty", "Case"]
    xml_2 = [seperate_semicolons(xml_string, semicolons) for xml_string in xml_1] 
    choice = ["DataRecord", "CompleteDataRecord", "SamplePreparation", "Procedure","SampleDimensions"]
    xml_3 = [keep_only_first_child(xml_string, choice) for xml_string in xml_2]
    xml_4 = [extract_single_xmls(xml, Tests) for xml in xml_3]
    xml_f = add_names(xml_4)
    return xml_f

