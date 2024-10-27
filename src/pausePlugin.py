# -*- coding: utf-8 -*-
# @Author: [Your Name]
# @Date:   [Current Date]
# @Description: Plugin to extract pauses from a transcript

from typing import List, Tuple
from GailBotTools import MarkerUtteranceDict
from GailBotTools import UtObj
from gailbot import Plugin

# Set default values if PAUSE_START and PAUSE_END are not present
PAUSE_START = getattr("PAUSE_START", "DEFAULT_PAUSE_START")
PAUSE_END = getattr("PAUSE_END", "DEFAULT_PAUSE_END")


class PauseDetectionPlugin(Plugin):
    """
    A plugin to detect pauses in the transcript based on utterance timings.
    """

    def __init__(self, threshold: float = 0.5):
        """
        Initializes the Pause Detection Plugin.

        Parameters
        ----------
        threshold: float
            The minimum duration (in seconds) to consider as a pause.
        """
        super().__init__()
        self.threshold = threshold
        self.pauses: List[Tuple[float, float]] = []

    def apply(self, data_structure: MarkerUtteranceDict):
        """
        Applies the pause detection logic to the given data structure.

        Parameters
        ----------
        data_structure: MarkerUtteranceDict
            The data structure containing utterances.

        Returns
        -------
        List[Tuple[float, float]]
            A list of tuples representing start and end times of pauses.
        """
        utterances = data_structure.list

        # Detect pauses and add markers to the data structure
        for i in range(1, len(utterances)):
            prev_utt = utterances[i - 1]
            current_utt = utterances[i]

            # Calculate the gap between the end of the previous utterance and the start of the current one
            gap = current_utt.start - prev_utt.end

            if gap > self.threshold:

                pause_start_marker = UttObj(
                    prev_utt.end,
                    prev_utt.end,
                    prev_utt.speaker,
                    PAUSE_START,
                    prev_utt.flexible_info,
                )
                pause_end_marker = UttObj(
                    current_utt.start,
                    current_utt.start,
                    current_utt.speaker,
                    PAUSE_END,
                    current_utt.flexible_info,
                )

                data_structure.insert_marker(pause_start_marker)
                data_structure.insert_marker(pause_end_marker)
                # If the gap is larger than the threshold, it's a pause
                self.pauses.append((prev_utt.end, current_utt.start))

        return self.pauses

    def get_pauses(self) -> List[Tuple[float, float]]:
        """
        Returns the detected pauses.

        Returns
        -------
        List[Tuple[float, float]]
            A list of tuples representing start and end times of pauses.
        """
        return self.pauses

    def testing_print(self, data_structure: MarkerUtteranceDict):
        """
        A testing function to print detected pauses.
        """
        print("Detected Pauses:")
        for start, end in self.pauses:
            print(f"Pause from {start} to {end}")

        # Call the XML print method
        data_structure.print_all_rows_xml(
            apply_subelement_root=lambda speaker: f"<Speaker>{speaker}</Speaker>",
            apply_subelement_word=lambda sentence, utt: print(f"<Word>{utt.text}</Word>"),
            apply_sentence_end=lambda sentence, start, end: print(f"<Sentence start='{start}' end='{end}'>{sentence}</Sentence>")
        )

