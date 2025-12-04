"""
Solution: state_machine

Key Insights:
1. match/case on (state, event) keeps transition logic compact.
2. State is updated then returned for convenience.
3. Unhandled events leave the state unchanged.

Alternative Approaches:
- Use a transition dict mapping (state, event) to next state.
"""

from __future__ import annotations


# === SOLUTION ===


class FSM:
    def __init__(self, initial_state="idle"):
        self._state = initial_state

    @property
    def state(self):
        return self._state

    def send(self, event: str) -> str:
        match (self._state, event):
            case ("idle", "start"):
                self._state = "running"
            case ("running", "stop"):
                self._state = "stopped"
            case ("stopped", "reset"):
                self._state = "idle"
            case _:
                pass
        return self._state


# === VERIFICATION ===


def test_transitions():
    fsm = FSM()
    assert fsm.state == "idle"
    assert fsm.send("start") == "running"
    assert fsm.send("stop") == "stopped"
    assert fsm.send("reset") == "idle"
    assert fsm.send("noop") == "idle"


if __name__ == "__main__":
    test_transitions()
    print("✅ test_transitions passed")
    print("\n🎉 All tests passed!")
