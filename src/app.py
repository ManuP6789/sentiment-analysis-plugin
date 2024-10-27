import sys
import os
from GailBotTools import StructureInteract
from pausePlugin import PauseDetectionPlugin
from client import Client

ID = 1

def run(data: str):
    # do whatever you'd like to the data
    # Load your XML data from a file
    xml_file_path = os.path.join('src', 'test', 'transcript.xml')  # Adjust the path if necessary
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Initialize StructureInteract and apply the XML data
    structure_interact = StructureInteract()
    structure_interact.apply(xml_data)

    # Create an instance of the PauseDetectionPlugin with a specific threshold
    pause_plugin = PauseDetectionPlugin(threshold=0.5)

    # Apply the pause detection to the data structure
    pauses = pause_plugin.apply(structure_interact.data_structure)

    # Print detected pauses
    pause_plugin.testing_print(structure_interact.data_structure)

def example():
    client = Client(ID, run)

    client.run_client()

if __name__ == "__main__":
    example()