"""
Challenge: state_machine
Difficulty: ⭐⭐⭐
Time Estimate: 20-25 minutes
Concepts: pattern matching, state transitions

Problem:
Implement a simple finite state machine (FSM) that processes events and updates
state. States: "idle", "running", "stopped". Events: "start", "stop", "reset".

Requirements:
1. FSM(initial_state="idle").send(event) returns new state and updates internal state.
2. Transitions:
   - idle + start -> running
   - running + stop -> stopped
   - stopped + reset -> idle
   - Any other event keeps state unchanged
3. Expose current state via .state property.

Hints:
- Use match/case on (state, event).

Run tests:
    python challenges/control_flow/challenge_03_state_machine.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


class FSM:
    def __init__(self, initial_state="idle"):
        raise NotImplementedError("Your implementation here")

    @property
    def state(self):
        raise NotImplementedError("Your implementation here")

    def send(self, event: str) -> str:
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_transitions():
    fsm = FSM()
    assert fsm.state == "idle"
    assert fsm.send("start") == "running"
    assert fsm.send("stop") == "stopped"
    assert fsm.send("reset") == "idle"
    assert fsm.send("noop") == "idle"


if __name__ == "__main__":
    import sys

    try:
        test_transitions()
        print("✅ test_transitions passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_transitions failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
