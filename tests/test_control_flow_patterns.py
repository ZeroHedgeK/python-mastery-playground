import pytest

from python_mastery.control_flow.advanced_flow import (
    demonstrate_for_else,
    demonstrate_pattern_matching,
    demonstrate_pipeline,
    find_first_prime,
    pipeline_errors,
    process_command,
)


def test_process_command_patterns():
    assert process_command(["load", "file.txt"]) == "Loading file.txt"
    assert (
        process_command({"action": "connect", "host": "h", "port": 80})
        == "Connecting to h:80"
    )
    assert process_command(["log", "a", "b"]) == "Log entries: a, b"
    assert process_command("quit") == "Exiting"
    assert process_command(["noop"]) == "Unknown command"


def test_pipeline_errors_skips_invalid():
    data = ["3", "bad", 4, "5.5", 8]
    # ints: 3, 4, 8 -> evens: 4, 8 -> squares: 16, 64
    assert pipeline_errors(data) == [16, 64]
    assert demonstrate_pipeline() == [16, 100]


def test_find_first_prime_and_for_else():
    assert find_first_prime([4, 6, 9, 11, 15]) == 11
    assert find_first_prime([4, 6, 8]) is None
    found, missing = demonstrate_for_else()
    assert found == 11
    assert missing is None


def test_demonstrate_pattern_matching_output():
    messages = demonstrate_pattern_matching()
    assert messages[0] == "Exiting"
    assert "Loading" in messages[1]
    assert messages[2].startswith("Connecting to")
    assert "Log entries" in messages[3]
    assert messages[4] == "Unknown command"
