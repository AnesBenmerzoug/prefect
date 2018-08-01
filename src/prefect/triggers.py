"""
Triggers are functions that determine if task state should change based on
the state of preceding tasks.
"""
from typing import TYPE_CHECKING, Dict, Iterable

from prefect.engine import signals

if TYPE_CHECKING:
    from prefect.engine.state import State
    from prefect.core import Task


def all_finished(upstream_states: Dict["Task", "State"]) -> bool:
    """
    This task will run no matter what the upstream states are, as long as they are finished.
    """
    if not all(s.is_finished() for s in upstream_states.values()):
        raise signals.TRIGGERFAIL(
            'Trigger was "all_finished" but some of the upstream tasks were not finished.'
        )

    return True


def manual_only(upstream_states: Dict["Task", "State"]) -> bool:
    """
    This task will never run automatically. It will only run if it is
    specifically instructed, either by ignoring the trigger or adding it
    as a flow run's start task.

    Note this doesn't raise a failure, it simply doesn't run the task.
    """
    raise signals.DONTRUN('Trigger function is "manual_only"')


# aliases
always_run = all_finished
never_run = manual_only


def all_successful(upstream_states: Dict["Task", "State"]) -> bool:
    """
    Runs if all upstream tasks were successful. Note that SKIPPED tasks are considered
    successes and TRIGGER_FAILED tasks are considered failures.
    """

    if not all(s.is_successful() for s in upstream_states.values()):
        raise signals.TRIGGERFAIL(
            'Trigger was "all_successful" but some of the upstream tasks failed.'
        )
    return True


def all_failed(upstream_states: Dict["Task", "State"]) -> bool:
    """
    Runs if all upstream tasks failed. Note that SKIPPED tasks are considered successes
    and TRIGGER_FAILED tasks are considered failures.
    """

    if not all(s.is_failed() for s in upstream_states.values()):
        raise signals.TRIGGERFAIL(
            'Trigger was "all_failed" but some of the upstream tasks succeeded.'
        )
    return True


def any_successful(upstream_states: Dict["Task", "State"]) -> bool:
    """
    Runs if any tasks were successful. Note that SKIPPED tasks are considered successes
    and TRIGGER_FAILED tasks are considered failures.
    """

    if not any(s.is_successful() for s in upstream_states.values()):
        raise signals.TRIGGERFAIL(
            'Trigger was "any_successful" but none of the upstream tasks succeeded.'
        )
    return True


def any_failed(upstream_states: Dict["Task", "State"]) -> bool:
    """
    Runs if any tasks failed. Note that SKIPPED tasks are considered successes and
    TRIGGER_FAILED tasks are considered failures.
    """

    if not any(s.is_failed() for s in upstream_states.values()):
        raise signals.TRIGGERFAIL(
            'Trigger was "any_failed" but none of the upstream tasks failed.'
        )
    return True