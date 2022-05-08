from water_logic.Challenge import Challenge
from water_logic.Jar import Jar


class ChallengeFactory:
    _challenges: [Challenge]
    _challenge_queue: [Challenge]

    def __init__(self) -> None:
        self._challenges = [
            Challenge(left_jar=Jar(capacity=2, goal=None), right_jar=Jar(capacity=3, goal=1), maximum_steps=2,
                      description="Preencher 1 no jarro direito."),
            Challenge(left_jar=Jar(capacity=6, goal=None), right_jar=Jar(capacity=4, goal=2), maximum_steps=2,
                      description="Preencher 2 no jarro direito."),
            Challenge(left_jar=Jar(capacity=7, goal=None), right_jar=Jar(capacity=5, goal=3), maximum_steps=2,
                      description="Preencher 3 no jarro direito."),
        ]
        self._challenge_queue = self._challenges.copy()

    def get_challenge(self):
        challenge = self._challenge_queue.pop()
        if len(self._challenge_queue) == 0:
            self._challenge_queue = self._challenges.copy()
        return challenge
