import sys
import os
from GailBotTools import StructureInteract
from pausePlugin import PausePlugin
from clients import Client

ID = 1

def run(data: str):

    # Initialize StructureInteract and apply the XML data
    structure_interact = StructureInteract()
    structure_interact.apply(data)

    # Create an instance of the PauseDetectionPlugin with a specific threshold
    pause_plugin = PausePlugin(threshold=0.5)

    # Apply the pause detection to the data structure
    pause_plugin.apply(structure_interact.data_structure)

    # Print detected pauses
    pause_plugin.testing_print(structure_interact.data_structure)

def example():
    client = Client(ID, run)

    client.run_client()

if __name__ == "__main__":
    example()