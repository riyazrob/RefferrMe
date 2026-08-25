from fastapi import HTTPException, status

from app.enums import STATUS_FLOW, TERMINAL_STATUSES, ReferralRequestStatus


def validate_status_transition(current: ReferralRequestStatus, new: ReferralRequestStatus) -> None:
    if current in TERMINAL_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition from terminal status '{current.value}'",
        )
    if new in TERMINAL_STATUSES:
        return
    try:
        current_idx = STATUS_FLOW.index(current)
        new_idx = STATUS_FLOW.index(new)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status") from exc
    if new_idx != current_idx + 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transition from '{current.value}' to '{new.value}'",
        )


def next_status(current: ReferralRequestStatus) -> ReferralRequestStatus | None:
    if current in TERMINAL_STATUSES:
        return None
    idx = STATUS_FLOW.index(current)
    if idx + 1 < len(STATUS_FLOW):
        return STATUS_FLOW[idx + 1]
    return None
