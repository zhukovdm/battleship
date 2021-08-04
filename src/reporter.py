class Reporter:
    """Reporter is used for reporting game state changes."""

    @staticmethod
    def report_invalid_input() -> None:
        print(" invalid input, try again")

    @staticmethod
    def report_player_name_is_too_long(len_allowed: int) -> None:
        print(" entered name is too long, only {} chars are allowed".format(len_allowed))

    @staticmethod
    def report_player_set(player_name: str) -> None:
        print()
        print(" {} has been set".format(player_name))

    @staticmethod
    def report_game_started() -> None:
        print()
        print(" the game has been started")

    @staticmethod
    def report_winner(winner_name: str) -> None:
        print(" {} wins, game over".format(winner_name))
