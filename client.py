"""Autonomous Errand Action Dispatcher.
100% Python Standard Library.
"""

import time

class ErrandActionDispatcher:
    """Manages life-admin errands with strict finite state machine (FSM) transitions."""
    VALID_TRANSITIONS = {
        "DRAFT": ["PENDING_APPROVAL", "DISPATCHED"],
        "PENDING_APPROVAL": ["DISPATCHED", "CANCELLED"],
        "DISPATCHED": ["IN_TRANSIT", "FAILED"],
        "IN_TRANSIT": ["COMPLETED", "FAILED"],
        "FAILED": ["REFUNDED", "RETRYING"],
        "RETRYING": ["DISPATCHED", "FAILED"],
        "COMPLETED": [],
        "REFUNDED": [],
        "CANCELLED": []
    }

    def __init__(self):
        self.errands = {}
        self.counter = 0

    def create_errand(self, task_type, details, requires_confirmation=False):
        self.counter += 1
        errand_id = f"ERRAND-{self.counter:04d}"
        initial_state = "PENDING_APPROVAL" if requires_confirmation else "DISPATCHED"
        record = {
            "errand_id": errand_id,
            "task_type": task_type,
            "details": details,
            "state": initial_state,
            "history": [(initial_state, "Initialization", time.time())]
        }
        self.errands[errand_id] = record
        return record

    def transition(self, errand_id, target_state, reason=""):
        if errand_id not in self.errands:
            raise KeyError(f"Errand {errand_id} not found")
        curr = self.errands[errand_id]["state"]
        allowed = self.VALID_TRANSITIONS.get(curr, [])
        if target_state not in allowed:
            raise ValueError(f"Illegal transition from {curr} to {target_state}. Allowed: {allowed}")
        
        self.errands[errand_id]["state"] = target_state
        self.errands[errand_id]["history"].append((target_state, reason, time.time()))
        return self.errands[errand_id]

    def get_summary(self, errand_id):
        e = self.errands[errand_id]
        return {
            "errand_id": e["errand_id"],
            "task": e["task_type"],
            "state": e["state"],
            "steps_count": len(e["history"])
        }
