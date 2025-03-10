"""
elepictl.py

Provides the ElePiCtl class to interact with the adventure.
Comes with a dbus service definition.
"""

import textwrap

from elepictl.adventure import Adventure

class ElePiCtl:
    """
    <node>
        <interface name='com.elepi.ElePiCtl'>
            <method name='info'><arg type='s' name='response' direction='out'/></method>
            <method name='hint'><arg type='s' name='response' direction='out'/></method>
            <method name='solve'>
                <arg type='s' name='solution_code' direction='in'/>
                <arg type='(bs)' name='msg' direction='out'/>
            </method>
            <method name='reset'><arg type='b' name='response' direction='out'/></method>
        </interface>
    </node>
    """

    def __init__(self):
        self._adventure = Adventure()

    # --- Private ---

    def _quest_info(self) -> str:
        quest_info = f"""
        Current quest: {self._adventure.active_quest.name}

        {self._adventure.active_quest.description}
        """
        return textwrap.dedent(quest_info)

    # --- Public ---

    def info(self) -> str:
        solved_count, total_count = self._adventure.progress
        general_info = f"""
        Welcome, brave soul, to this learning adventure!
        
        A sequence of thrilling quests awaits you. On each quest, you'll learn something
        about Embedded Linux development while searching for a unique solution code required
        to progress to the next one.

        The solution code is a 512 digit hexadecimal number that you need to pass to the
        'solve' command to complete the quest. Note that you may have to collect several
        fragments to assemble the solution code.

        So far, you have solved {solved_count} of {total_count} quests in this adventure.
        ____________________________________________________________________________________
        """
        return textwrap.dedent(general_info + self._quest_info())
    
    def hint(self) -> str:
        return self._adventure.active_quest.next_hint

    def solve(self, solution_code: str) -> tuple[bool, str]:
        # TODO: Extend failure handling here
        if not self._adventure.active_quest.verify(solution_code):
            return False, "Sorry, this is not correct yet - try again ;)"
        
        msg = "Congratulations! You have solved the quest!\n"

        if not self._adventure.activate_next_quest():
            msg += """
            ...even better: You have completed all quests!

            You are now ready for the next adventure.
            """
            return True, msg

        msg += "The next quest is already waiting for you:\n"
        return True, textwrap.dedent(msg + self._quest_info())


    def reset(self) -> bool:
        # TODO: Add failure handling here
        self._adventure.reset_quest()
        return True