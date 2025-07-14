from lib.adb_wrapper import ADBWrapper
import xml.etree.ElementTree as ET

def parse_ui_xml(xml_string: str) -> ET.Element:
    """Parse the UI XML string into an ElementTree Element.

    Args:
        xml_string (str): The XML string to parse.

    Returns:
        ET.Element: The root element of the parsed XML.
    """
    try:
        root = ET.fromstring(xml_string)
        return root
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse XML: {e}")

def print_ui_hierarchy(element: ET.Element, indent: str = ""):
    """Recursively print the UI hierarchy from an ElementTree Element.

    Args:
        element (ET.Element): The root element of the UI hierarchy.
        indent (str): Indentation string for pretty printing.
    """
    print(f"{indent}<{element.tag} {element.attrib.get('text', "")}>")
    for child in element:
        print_ui_hierarchy(child, indent + "  ")
    print(f"{indent}</{element.tag}>")

def main():
    adb = ADBWrapper("/home/lumonis/Code/DBL-Automate/platform-tools/adb")
    devices = adb.list_devices()
    xml_str = adb.dump_ui_xml(devices[0])
    root = parse_ui_xml(xml_str)
    print("==================")
    print_ui_hierarchy(root)


if __name__ == "__main__":
    main()
