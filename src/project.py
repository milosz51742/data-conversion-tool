import argparse
import json
import yaml
import xml.etree.ElementTree as ET
from jsonschema import validate as json_validate
import os

# (Task1)
def parse_arguments():
    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('--input', type=str, required=True, help='Input file path')
    parser.add_argument('--output', type=str, required=True, help='Output file path')
    parser.add_argument('--format', type=str, choices=['json', 'yaml', 'xml'], required=True, help='File format')
    return parser.parse_args()

# (Task2, Task3)
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def validate_json(data, schema):
    try:
        json_validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(f'JSON validation error: {err}')
        return False
    return True

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# (Task4, Task5)
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def validate_yaml(data, schema):
    try:
        json_validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(f'YAML validation error: {err}')
        return False
    return True

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# (Task6, Task7)
def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def save_xml(data, file_path):
    tree = ET.ElementTree(data)
    tree.write(file_path)

def convert_to_dict(element):
    return {element.tag: {child.tag: child.text for child in element}}

def convert_to_element(data, root_tag):
    root = ET.Element(root_tag)
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return root

if __name__ == "__main__":
    args = parse_arguments()
  
    if args.format == 'json':
        data = load_json(args.input)
    elif args.format == 'yaml':
        data = load_yaml(args.input)
    elif args.format == 'xml':
        data = load_xml(args.input)
        data = convert_to_dict(data)

    if args.format == 'json':
        save_json(data, args.output)
    elif args.format == 'yaml':
        save_yaml(data, args.output)
    elif args.format == 'xml':
        data_element = convert_to_element(data, 'root')  # Replace 'root' with the appropriate tag
        save_xml(data_element, args.output)
