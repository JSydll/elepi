"""
adventure.py

This module provides classes and functions to manage and interact with an adventure 
consisting of multiple quests. It includes functionality to load, save, and manage 
the state of quests within an adventure.

"""

import json
import warnings

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from elepictl.abstractions.packages import PackageManager
from elepictl.abstractions.verification import Verification

_DATA_DIR = Path('/usr/share/elepi')
_ADVENTURE_DIR = _DATA_DIR / 'adventure'
_QUEST_DIR = _DATA_DIR / 'quest'

_ADVENTURE_META_FILE = _ADVENTURE_DIR / 'meta.json'
_ADVENTURE_SOLUTION_TOKEN = _ADVENTURE_DIR / 'solution.token'
_ADVENTURE_QUESTS_DIR = _ADVENTURE_DIR / 'quests'

_QUEST_DESCRIPTION_FILE = _QUEST_DIR / 'description.txt'
_QUEST_VERIFICATION_KEY = _QUEST_DIR / 'verification.key'
_QUEST_HINTS_DIR = _QUEST_DIR / 'hints'


@dataclass
class QuestState:
    """
    QuestState represents the state of a quest in the current adventure.
    Attributes:
        name: The name of the quest (also used to identify its package).
        sequence_number: Indicates the order in which the quests shall be solved.
        solved: Indicates whether the quest has been solved. Defaults to False.
    """
    name: str
    sequence_number: int
    solved: bool = False


class ActiveQuest:
    """
    Represents an active quest in the current adventure.

    Provides information about the quest as well as means to verify a solution.
    """

    def __init__(self, name: str):
        self._name = name
        self._hint_files = sorted(_QUEST_HINTS_DIR.glob('*.txt'))
        self._current_hint_index = 0

    # --- Public ---

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        """
        Reads out the description file for the quest.

        Returns:
            The description of the quest or a default message.
        """
        if _QUEST_DESCRIPTION_FILE.exists():
            return _QUEST_DESCRIPTION_FILE.read_text()
        else:
            return "No description for this quest available - this may be a bug."

    @property
    def next_hint(self) -> str:
        """
        Provides the next available hint on solving the quest.

        Returns:
            The next hint if available, otherwise a message indicating no more hints are left.
        """

        if self._current_hint_index < len(self._hint_files):
            hint = self._hint_files[self._current_hint_index].read_text()
            self._current_hint_index += 1
            return hint
        else:
            return "Sorry, no more hints available. Maybe ask the community for help?"

    def verify(self, solution_code: str) -> bool:
        """
        Verifies the provided solution code against the quest's verification key.

        Args:
            solution_code: A hex code representing the solution signature.

        Returns:
            bool: True if the solution code is verified successfully, false otherwise.
        """

        key_path = str(_QUEST_VERIFICATION_KEY)
        token_path = str(_ADVENTURE_SOLUTION_TOKEN)

        signature = Verification.get_signature(solution_code)
        return Verification.check_signature(signature, key_path, token_path)


class Adventure:
    """
    Represents an adventure consisting of multiple quests.
    """
    _meta_file_path: Path
    _name: str
    _active_quest: Optional[ActiveQuest]
    _quest_states: list[QuestState]

    # --- Private ---

    def __init__(self, meta_file_path: Path = _ADVENTURE_META_FILE):
        self._meta_file_path = meta_file_path
        self._active_quest = None
        self.load(self._meta_file_path)

    def _find_quest_state(self, quest_name: str) -> Optional[QuestState]:
        for quest in self._quest_states:
            if quest.name == quest_name:
                return quest
        return None

    def _install_quest(self, quest_name: str) -> None:
        local_package_path = _ADVENTURE_QUESTS_DIR / f"{quest_name}.rpm"
        PackageManager.install(local_package_path)

    # --- Public ---

    def load(self, file_path: Path = _ADVENTURE_META_FILE) -> None:
        """
        Loads adventure data from the meta data file stored on disk.

        It also selects the first unsolved quest as active quest.

        Args:
            file_path: The path to the JSON file containing adventure data.
                       Defaults to _ADVENTURE_META_FILE.
        """

        if not file_path.exists():
            raise RuntimeError("Adventure seems not to be properly installed!")

        current_quest_name: Optional[str] = None
        self._quest_states = []
        with file_path.open('r') as f:
            data = json.load(f)
            self._name = data['name']
            for i, quest in enumerate(data['quests']):
                self._quest_states.append(QuestState(
                    quest['name'], i, quest['solved']))
                # The first unsolved quest is the current quest
                if current_quest_name is None and not quest['solved']:
                    current_quest_name = quest['name']

        if current_quest_name is None:
            warnings.warn("No active quest found!")
            return

        self._active_quest = ActiveQuest(current_quest_name)

    @property
    def active_quest(self) -> ActiveQuest:
        return self._active_quest

    @property
    def progress(self) -> tuple[int, int]:
        """
        Provides the current progress of the adventure.

        Returns:
            tuple(int, int): A tuple containing the number of solved quests and the total number of quests.
        """
        solved_quests = sum(quest.solved for quest in self._quest_states)
        return solved_quests, len(self._quest_states)

    def reset_quest(self):
        """
        Resets the current quest by removing and reinstalling it.

        This can be useful for restarting the quest from the beginning or resetting its state.
        """
        PackageManager.remove(self._active_quest.name)
        self._install_quest(self._active_quest.name)

    def activate_next_quest(self) -> bool:
        """
        Activates the next quest in the adventure sequence.

        This method marks the current quest as solved and installs the next quest in the sequence.

        Returns:
            bool: True if the next quest was successfully activated, false if there are no more quests in the sequence.

        Raises:
            RuntimeError: If there is no active quest or if the current quest cannot be found in the adventure.
        """

        if not self._active_quest:
            raise RuntimeError("No active quest found!")

        current_quest_state = self._find_quest_state(self._active_quest.name)
        if current_quest_state is None:
            raise RuntimeError("Could not find the quest in this adventure!")

        current_quest_state.solved = True

        self.save(self._meta_file_path)

        if len(self._quest_states) == current_quest_state.sequence_number + 1:
            return False

        PackageManager.remove(self._active_quest.name)
        next_quest_state = self._quest_states[current_quest_state.sequence_number + 1]
        self._install_quest(next_quest_state.name)
        self._active_quest = ActiveQuest(next_quest_state.name)
        return True

    def save(self, file_path: Path = _ADVENTURE_META_FILE):
        """
        Save the current adventure state to a JSON file.

        Args:
            file_path: The path to the file where the adventure state will be saved.
                       Defaults to overwriting the _ADVENTURE_META_FILE.
        """
        data = {
            'name': self._name,
            'quests': [quest.__dict__ for quest in self._quest_states]
        }
        with file_path.open('w') as f:
            json.dump(data, f, indent=4)
