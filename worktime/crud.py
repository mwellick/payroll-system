from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database.models import WorkTime
from .schemas import WorkTimeCreated


def check_worktime_exists_by_id(worktime_id, db):
    """
    This function checks if specific worktime exists
    """
    query = select(WorkTime).where(
        WorkTime.id == worktime_id
    ).options(
        joinedload(WorkTime.employee)
    )
    result = db.execute(query)
    worktime_instance = result.scalars().first()

    if not worktime_instance:
        raise HTTPException(
            detail="Worktime not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return worktime_instance


def check_worktime_exists(worktime, db):
    """
    Check if the employee already has a worktime
    entry for the given date.
    """
    query = select(WorkTime).where(
        WorkTime.employee_id == worktime.employee_id,
        WorkTime.work_date == worktime.work_date
    )
    result = db.execute(query)
    exists = result.scalars().first()

    if exists:
        raise HTTPException(
            detail="This employee already has a worktime record for this date",
            status_code=status.HTTP_400_BAD_REQUEST
        )


def worktime_create(db, worktime):
    check_worktime_exists(worktime, db)

    worktime_instance = WorkTime(
        employee_id=worktime.employee_id,
        work_date=worktime.work_date,
        hours_worked=worktime.hours_worked,
        is_weekend=worktime.is_weekend,
        is_holiday=worktime.is_holiday
    )
    db.add(worktime_instance)
    db.commit()
    db.refresh(worktime_instance)

    return WorkTimeCreated.model_validate(worktime_instance)


def get_list_worktimes(db):
    query = select(WorkTime).options(
        joinedload(WorkTime.employee)
    )
    result = db.execute(query)
    return result.scalars().all()


def worktime_update(worktime_id, db, worktime):
    worktime_instance = check_worktime_exists_by_id(worktime_id, db)

    update_data = worktime.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(worktime_instance, k, v)

    db.commit()
    db.refresh(worktime_instance)

    return {
        "message": f"Worktime of employee ID: "
                   f"{worktime_instance.employee_id} "
                   f"was updated successfully"
    }

def worktime_delete(worktime_id, db):
    worktime_instance = check_worktime_exists_by_id(worktime_id, db)

    db.delete(worktime_instance)
    db.commit()

    return
