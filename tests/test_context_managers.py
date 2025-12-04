"""
test_context_managers.py - Unit tests for the context_managers module.

Tests cover:
- Timer (class-based context manager)
- timer_context (generator-based context manager)
- env_var (temporary environment variable)
- Reusable / SingleUse (reentrant patterns)
"""

import os
import time

import pytest

from python_mastery.context_managers import (
    Reusable,
    Timer,
    env_var,
    timer_context,
)
from python_mastery.context_managers.reentrant import SingleUse


class TestTimerClassBased:
    """Tests for the class-based Timer context manager."""

    def test_timer_measures_elapsed_time(self):
        """Timer should measure elapsed time correctly."""
        with Timer() as timer:
            time.sleep(0.1)

        assert timer.elapsed is not None
        assert timer.elapsed >= 0.1
        assert timer.elapsed < 0.2  # Allow some overhead

    def test_timer_with_name(self, capsys):
        """Timer should include name in output when provided."""
        with Timer("test_operation"):
            pass

        output = capsys.readouterr().out
        assert "test_operation" in output
        assert "seconds" in output

    def test_timer_without_name(self, capsys):
        """Timer should work without a name."""
        with Timer():
            pass

        output = capsys.readouterr().out
        assert "Timer" in output
        assert "seconds" in output

    def test_timer_elapsed_during_execution(self):
        """Timer.elapsed should work during context execution."""
        with Timer() as timer:
            time.sleep(0.05)
            mid_elapsed = timer.elapsed
            time.sleep(0.05)

        # Mid-execution elapsed should be roughly half of total
        assert mid_elapsed is not None
        assert mid_elapsed >= 0.05
        assert timer.elapsed >= 0.1

    def test_timer_elapsed_before_start(self):
        """Timer.elapsed should be None before entering context."""
        timer = Timer()
        assert timer.elapsed is None

    def test_timer_propagates_exceptions(self):
        """Timer should not swallow exceptions."""
        with pytest.raises(ValueError, match="test error"):
            with Timer() as timer:
                raise ValueError("test error")

        # Timer should still record elapsed time
        assert timer.elapsed is not None

    def test_timer_records_time_on_exception(self, capsys):
        """Timer should print timing even when exception occurs."""
        try:
            with Timer("exception_test"):
                time.sleep(0.05)
                raise RuntimeError("Oops")
        except RuntimeError:
            pass

        output = capsys.readouterr().out
        assert "exception_test" in output
        assert "seconds" in output


class TestTimerContext:
    """Tests for the generator-based timer_context."""

    def test_timer_context_basic(self, capsys):
        """timer_context should print elapsed time."""
        with timer_context():
            time.sleep(0.05)

        output = capsys.readouterr().out
        assert "Timer" in output
        assert "seconds" in output

    def test_timer_context_with_name(self, capsys):
        """timer_context should include name in output."""
        with timer_context("named_operation"):
            pass

        output = capsys.readouterr().out
        assert "named_operation" in output

    def test_timer_context_propagates_exceptions(self):
        """timer_context should not swallow exceptions."""
        with pytest.raises(ZeroDivisionError):
            with timer_context():
                _ = 1 / 0

    def test_timer_context_records_on_exception(self, capsys):
        """timer_context should print timing even on exception."""
        try:
            with timer_context("error_case"):
                raise KeyError("missing")
        except KeyError:
            pass

        output = capsys.readouterr().out
        assert "error_case" in output

    def test_timer_context_nested(self, capsys):
        """timer_context should work when nested."""
        with timer_context("outer"):
            time.sleep(0.02)
            with timer_context("inner"):
                time.sleep(0.02)

        output = capsys.readouterr().out
        assert "outer" in output
        assert "inner" in output


class TestEnvVar:
    """Tests for the env_var context manager."""

    def test_env_var_sets_value(self, clean_env):
        """env_var should set the environment variable."""
        assert os.environ.get("TEST_VAR") is None

        with env_var("TEST_VAR", "test_value"):
            assert os.environ.get("TEST_VAR") == "test_value"

    def test_env_var_restores_on_exit(self, clean_env):
        """env_var should restore original value on exit."""
        os.environ["EXISTING_VAR"] = "original"

        with env_var("EXISTING_VAR", "temporary"):
            assert os.environ["EXISTING_VAR"] == "temporary"

        assert os.environ["EXISTING_VAR"] == "original"

    def test_env_var_deletes_if_not_existed(self, clean_env):
        """env_var should delete the variable if it didn't exist before."""
        key = "NEW_VAR_FOR_TEST"
        assert os.environ.get(key) is None

        with env_var(key, "temporary"):
            assert os.environ.get(key) == "temporary"

        assert os.environ.get(key) is None

    def test_env_var_nested(self, clean_env):
        """env_var should work correctly when nested."""
        key = "NESTED_VAR"

        with env_var(key, "level1"):
            assert os.environ[key] == "level1"

            with env_var(key, "level2"):
                assert os.environ[key] == "level2"

            assert os.environ[key] == "level1"

        assert os.environ.get(key) is None

    def test_env_var_restores_on_exception(self, clean_env):
        """env_var should restore value even if exception occurs."""
        os.environ["EXCEPTION_VAR"] = "original"

        try:
            with env_var("EXCEPTION_VAR", "temporary"):
                assert os.environ["EXCEPTION_VAR"] == "temporary"
                raise ValueError("test error")
        except ValueError:
            pass

        assert os.environ["EXCEPTION_VAR"] == "original"


class TestReusable:
    """Tests for the Reusable context manager."""

    def test_reusable_can_be_used_multiple_times(self):
        """Reusable should allow multiple entries."""
        reusable = Reusable()

        with reusable:
            pass

        with reusable:
            pass

        with reusable:
            pass

        assert reusable.count == 3

    def test_reusable_tracks_usage_count(self):
        """Reusable should track how many times it's been used."""
        reusable = Reusable()

        assert reusable.count == 0

        with reusable:
            assert reusable.count == 1

        with reusable:
            assert reusable.count == 2

    def test_reusable_prints_usage_info(self, capsys):
        """Reusable should print entry/exit messages with count."""
        reusable = Reusable()

        with reusable:
            pass

        output = capsys.readouterr().out
        assert "Entering Reusable" in output
        assert "Exiting Reusable" in output
        assert "#1" in output


class TestSingleUse:
    """Tests for the SingleUse context manager."""

    def test_single_use_works_once(self, capsys):
        """SingleUse should work on first use."""
        single = SingleUse()

        with single:
            pass

        output = capsys.readouterr().out
        assert "Entering SingleUse" in output
        assert "Exiting SingleUse" in output

    def test_single_use_fails_on_reuse(self):
        """SingleUse should raise RuntimeError on second use."""
        single = SingleUse()

        with single:
            pass

        with pytest.raises(RuntimeError, match="Cannot reuse"):
            with single:
                pass

    def test_single_use_tracks_used_state(self):
        """SingleUse should track whether it's been used."""
        single = SingleUse()

        assert single.used is False

        with single:
            assert single.used is True

        assert single.used is True


class TestTimerIntegration:
    """Integration tests combining timer functionality."""

    def test_multiple_sequential_timers(self, capsys):
        """Multiple timers should work independently."""
        with Timer("first") as t1:
            time.sleep(0.05)

        with Timer("second") as t2:
            time.sleep(0.03)

        assert t1.elapsed >= 0.05
        assert t2.elapsed >= 0.03
        assert t1.elapsed > t2.elapsed

        output = capsys.readouterr().out
        assert "first" in output
        assert "second" in output

    def test_timer_with_env_var(self, clean_env, capsys):
        """Timer and env_var should work together."""
        with Timer("config_operation"):
            with env_var("CONFIG_VAR", "test_value"):
                assert os.environ["CONFIG_VAR"] == "test_value"
                time.sleep(0.02)

        assert os.environ.get("CONFIG_VAR") is None
        output = capsys.readouterr().out
        assert "config_operation" in output


class TestContextManagerEdgeCases:
    """Edge case tests for context managers."""

    def test_timer_zero_duration(self, capsys):
        """Timer should handle zero-duration operations."""
        with Timer("instant"):
            pass

        output = capsys.readouterr().out
        assert "instant" in output
        # Should show very small time (close to 0)

    def test_env_var_empty_string(self, clean_env):
        """env_var should handle empty string values."""
        with env_var("EMPTY_VAR", ""):
            assert os.environ.get("EMPTY_VAR") == ""

        assert os.environ.get("EMPTY_VAR") is None

    def test_env_var_special_characters(self, clean_env):
        """env_var should handle special characters in values."""
        special_value = "hello=world&foo=bar"

        with env_var("SPECIAL_VAR", special_value):
            assert os.environ.get("SPECIAL_VAR") == special_value

    def test_timer_returns_self(self):
        """Timer.__enter__ should return self for 'as' clause."""
        timer = Timer("test")

        with timer as t:
            assert t is timer

    def test_reusable_nested_usage(self):
        """Reusable should handle nested usage correctly."""
        reusable = Reusable()

        with reusable:
            with reusable:
                with reusable:
                    pass

        assert reusable.count == 3
