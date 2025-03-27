'''
elepictl.py

Provides the ElePiCtl class to interact with the adventure.
Comes with a dbus service definition.
'''

from elepictl.adventure import Adventure


class ElePiCtl:
    """
    <node>
        <interface name='com.elepi.ElePiCtl'>
            <method name='status'><arg type='s' name='response' direction='out'/></method>
            <method name='hint'><arg type='s' name='response' direction='out'/></method>
            <method name='verify_quest'>
                <arg type='s' name='solution_code' direction='in'/>
                <arg type='(bs)' name='response' direction='out'/>
            </method>
            <method name='complete_quest'>
                <arg type='(bs)' name='response' direction='out'/>
            </method>
            <method name='reset_quest'><arg type='b' name='response' direction='out'/></method>
        </interface>
    </node>
    """

    def __init__(self):
        self._adventure = Adventure()
        self._allow_completion = False

    # --- Private ---

    def _quest_info(self) -> str:
        quest_info = (f'Current quest: {self._adventure.active_quest.name}\n\n'
                      f'{self._adventure.active_quest.description}\n')
        return quest_info

    # --- Public ---

    def status(self) -> str:
        general_info = ("Welcome, brave soul, to this learning adventure!\n\n"
                        "A sequence of thrilling quests awaits you. On each quest, "
                        "you'll learn something about Embedded Linux development while "
                        "searching for a unique solution code required to progress "
                        "to the next one.\n\n"
                        "The solution code is a 512 digit hexadecimal number "
                        "that you need to pass to the 'solve' command to complete the quest. "
                        "Note that you may have to collect several fragments to assemble "
                        "the solution code.\n\n")

        solved_count, total_count = self._adventure.progress
        msg = general_info
        if solved_count != total_count:
            msg += (f'So far, you have solved {solved_count} of {total_count} quests in this adventure.\n\n'
                    '====\n\n')
            msg += self._quest_info()
        else:
            msg += f'But what do I tell you - you already solved all quests in this adventure!\n'

        return msg

    def hint(self) -> str:
        return self._adventure.active_quest.next_hint

    def verify_quest(self, solution_code: str) -> tuple[bool, str]:
        # TODO: Extend failure handling here
        if not self._adventure.active_quest.verify(solution_code):
            return False, 'Sorry, this is not correct yet - try again ;)\n'

        self._allow_completion = True
        return True, 'Congratulations! You have solved the quest!\n'

    def complete_quest(self) -> tuple[bool, str]:
        # TODO: Extend failure handling here
        if not self._allow_completion:
            return False, "The current quest has not yet been solved (this shouldn't happen).\n"

        self._allow_completion = False
        msg = ''
        if not self._adventure.activate_next_quest():
            msg += ('...even better: You have completed all quests!\n\n'
                    'You are now ready for the next adventure.\n')
            return True, msg

        msg += 'The next quest is already waiting for you:\n\n'
        return True, msg + self._quest_info()

    def reset_quest(self) -> bool:
        # TODO: Add failure handling here
        self._adventure.reset_quest()
        return True
