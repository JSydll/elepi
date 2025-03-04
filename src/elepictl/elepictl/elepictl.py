from elepictl.adventure import Adventure

class ElePiCtl:

    def __init__(self):
        self._adventure = Adventure()

    # --- Private ---

    def _quest_info(self) -> None:
        quest_info = f"""
        Current quest: {self._adventure.active_quest.name}

        {self._adventure.active_quest.description}
        """
        print(quest_info)

    # --- Public ---

    def info(self) -> None:
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

        """
        print(general_info)
        self._quest_info()
    
    def hint(self) -> None:
        hint = self._adventure.active_quest.next_hint
        print(hint)


    def solve(self, solution_code: str) -> None:
        if not self._adventure.active_quest.verify(solution_code):
            print("Sorry, this is not correct yet - try again ;)")
            return
        
        print("Congratulations! You have solved the quest!\n")

        if not self._adventure.activate_next_quest():
            msg = """
            ...even better: You have completed all quests!

            You are now ready for the next adventure.
            """
            print(msg)
            return

        print("The next quest is already waiting for you:\n")
        self._quest_info()


    def reset(self) -> None:
        print("""
        Resetting the state of the current quest...
        Note that any changes not belonging to the quest might stay around.
        """)
        self._adventure.reset_quest()
        print("Done! You can start tinkering again.")