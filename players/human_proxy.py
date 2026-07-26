"""Main-process proxy that talks to human_player subprocess."""

from __future__ import annotations

from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision, Observation
from protocols.subprocess_transport import (
    HumanProcessError,
    HumanTimeoutError,
    SubprocessTransport,
)


class HumanPlayerProxy(BasePlayer):
    """BasePlayer implementation living in the engine process."""

    def __init__(
        self,
        name: str = "",
        player_id: str | None = None,
        *,
        seed: int | None = None,
        training_mode: bool = False,
        theme: str = "green",
        timeout_ms: int = 120_000,
    ) -> None:
        super().__init__(
            name=name or "Human",
            player_id=player_id,
            seed=seed,
            training_mode=training_mode,
        )
        self.theme = theme
        self.timeout_ms = timeout_ms
        self._transport: SubprocessTransport | None = None
        # False when transport is owned by SeatUIHub (must not kill on game end)
        self._owns_transport: bool = False

    def attach_transport(self, transport: SubprocessTransport, seat: int) -> None:
        """Use a seat window already started by SeatUIHub (hub owns process)."""
        self._transport = transport
        self._owns_transport = False
        self.seat = seat
        if not self.name or self.name == "Human":
            self.name = f"Human-{seat}"

    def on_join(self, seat: int, config: dict) -> None:
        self.seat = seat
        self.config.update(dict(config or {}))
        if self._transport is not None:
            # Already attached by SeatUIHub or previous join
            if not self.name or self.name == "Human":
                self.name = f"Human-{seat}"
            return
        theme = str(self.config.get("theme", self.theme))
        timeout = int(self.config.get("human_timeout_ms", self.timeout_ms))
        num_players = int(self.config.get("num_players", 4))
        extra: list[str] = ["--mode", "play", "--num-players", str(num_players)]
        try:
            from display.window_geometry import (
                plan_cli_args,
                plan_for_screen,
                rect_from_plan_dict,
            )

            rect = None
            wp = self.config.get("window_plan")
            if isinstance(wp, dict):
                rect = rect_from_plan_dict(wp, seat)
            if rect is None:
                # F0018: this seat is human play path
                plan = plan_for_screen(num_players, human_seats=[seat])
                rect = plan.players.get(seat)
            if rect is not None:
                extra = plan_cli_args(rect) + extra
        except Exception:
            pass
        self._transport = SubprocessTransport(
            seat,
            theme=theme,
            timeout_ms=timeout,
            extra_args=extra,
            module="players.seat_window",
        )
        hello = self._transport.start()
        self._owns_transport = True
        if not self.name or self.name == "Human":
            self.name = f"Human-{seat}"
        self.config["human_pid"] = hello.get("pid")

    def observe(self, observation: Observation) -> None:
        super().observe(observation)
        if self._transport is None:
            raise HumanProcessError("human not joined")
        self._transport.send_observation(observation)

    def decide(self, request: ActionRequest) -> Decision:
        if self._transport is None:
            raise HumanProcessError("human not joined")
        hints = None
        # Optional analysis from engine state if attached
        state = getattr(self, "_engine_state", None)
        if state is not None and request.phase == "discard":
            try:
                from engine.action import ActionType
                from engine.legal import legal_actions
                from players.analysis.pipeline import analyze_for_seat

                legal = legal_actions(state, request.seat)
                discs = [a for a in legal if a.type == ActionType.DISCARD]
                # A5: F0011 when env F0011=1 or proxy.use_f0011
                use_f = getattr(self, "use_f0011", None)
                snap = analyze_for_seat(
                    state,
                    request.seat,
                    legal_discards=discs,
                    use_f0011=use_f,
                )
                hints = snap.to_dict(verbose=True)
                hints["use_f0011"] = bool(getattr(snap, "use_f0011", False))
                if snap.discard_ranks:
                    best = snap.discard_ranks[0]
                    hints["f0011_best"] = best.tile_id
                    hints["f0011_danger"] = best.danger
                    det = getattr(best, "f0011_detail", None)
                    if det:
                        hints["f0011_detail"] = det
                    # F0012: precompute display recommendations for seat window
                    from players.analysis.discard_recommend import (
                        build_discard_recommendations,
                    )

                    hints["recommendations"] = build_discard_recommendations(
                        snap.discard_ranks
                    )
            except Exception:
                hints = None
        return self._transport.request_decision(request, hints=hints)

    def on_game_end(self, result: dict) -> None:
        if self._transport:
            self._transport.send_game_end(result)

    def shutdown(self) -> None:
        # Only kill process if this proxy spawned it; hub-owned stays open.
        if self._transport is not None and self._owns_transport:
            try:
                self._transport.shutdown()
            except Exception:
                pass
            self._transport = None
            self._owns_transport = False
