"""Mechanical GP/RP traceability registry for F0028."""

from __future__ import annotations

from dataclasses import dataclass

from players.humanlike.config import GP_IDS
from players.humanlike.runtime import RP_IDS


@dataclass(frozen=True, slots=True)
class ParameterTrace:
    parameter_id: str
    schema_path: str
    consumer: str
    test_anchor: str


def _gp_consumer(index: int) -> str:
    if index <= 10:
        return "match_engine_adapter"
    if index <= 20:
        return "scoring_adapter"
    if index <= 22:
        return "player_view_timeout"
    if index == 23:
        return "player_profile"
    return "humanlike_policy"


def _rp_consumer(index: int) -> str:
    if index <= 3:
        return "round_initializer"
    if index <= 12:
        return "round_view_state"
    if index <= 15:
        return "decision_context"
    if index <= 22:
        return "analysis_plan"
    if index <= 28:
        return "cognitive_policy"
    return "audit_settlement_learning"


PARAMETER_TRACES: tuple[ParameterTrace, ...] = tuple(
    ParameterTrace(parameter_id, (f"global_parameters.{parameter_id}" if index <= 23 else f"players[i].cognitive_parameters.{parameter_id}"), _gp_consumer(index), "tests/humanlike_v2/test_config.py")
    for index, parameter_id in enumerate(GP_IDS, 1)
) + tuple(
    ParameterTrace(parameter_id, f"round_parameters.{parameter_id}", _rp_consumer(index), "tests/humanlike_v2/test_runtime.py")
    for index, parameter_id in enumerate(RP_IDS, 1)
)


TRACE_BY_ID = {trace.parameter_id: trace for trace in PARAMETER_TRACES}

if len(PARAMETER_TRACES) != 60 or len(TRACE_BY_ID) != 60:
    raise RuntimeError("F0028 parameter trace registry must contain 60 unique GP/RP entries")
