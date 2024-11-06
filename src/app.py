import sys
import os
from GailBotTools import StructureInteract
from pausePlugin import PausePlugin
from clients import Client
from gailbot import GBPluginMethods

ID = 1

def run(data: str):

    # Initialize StructureInteract and apply the XML data
    structure_interact = StructureInteract()
    structure_interact.apply(data)

    # Create an instance of the PauseDetectionPlugin with a specific threshold
    pause_plugin = PausePlugin()

    methods = GBPluginMethods("", "", "", "", "")

    gap_output = {"GapPlugin": structure_interact}
    # Apply the pause detection to the data structure
    pause_plugin.apply(gap_output, methods)

    # Print detected pauses
    print(f"PRINTS HERE. MAKES IT PAST .APPLY() {pause_plugin}")
    pause_plugin.testing_print()

def example():
    client = Client(ID, run)

    client.run_client()

if __name__ == "__main__":
    example()