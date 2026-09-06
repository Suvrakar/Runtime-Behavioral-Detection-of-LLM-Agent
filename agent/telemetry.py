"""TRACE telemetry logger — wraps every tool call and writes trajectory JSON."""
import json
import time
from pathlib import Path


class TelemetryLogger:
    """Wraps tool calls, accumulates a trajectory, writes it to disk on close."""

    def __init__(
        self,
        run_id: str,
        instance_id: str,
        seed: int,
        model: str,
        label: str,
        attack_type,
        task_description: str,
        split: str,
        out_dir: str = "data/trajectories",
    ):
        self.run_id = run_id
        self.out_dir = Path(out_dir)
        self.meta = {
            "run_id": run_id,
            "instance_id": instance_id,
            "seed": seed,
            "model": model,
            "label": label,
            "attack_type": attack_type,
            "task_description": task_description,
            "split": split,
            "steps": [],
            "final_action": None,
            "attack_succeeded": None,
            "total_steps": 0,
            "wall_clock_ms": 0,
        }
        self.start_ms = int(time.time() * 1000)

    def log_step(
        self,
        tool: str,
        args: dict,
        result_ok: bool,
        result_summary: str = "",
    ) -> None:
        self.meta["steps"].append(
            {
                "step_id": len(self.meta["steps"]),
                "tool": tool,
                "args": args,
                "result_ok": result_ok,
                "result_summary": str(result_summary)[:200],
                "ts_ms": int(time.time() * 1000),
            }
        )

    def close(self, final_action: str, attack_succeeded: bool) -> dict:
        self.meta["final_action"] = final_action
        self.meta["attack_succeeded"] = attack_succeeded
        self.meta["total_steps"] = len(self.meta["steps"])
        self.meta["wall_clock_ms"] = int(time.time() * 1000) - self.start_ms

        out_path = self.out_dir / self.meta["label"] / f"{self.run_id}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(self.meta, indent=2))
        return self.meta
