from datetime import date
from decimal import Decimal
from sqlalchemy import ForeignKey, String, Date, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.engine import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tab_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(64), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    passport_id: Mapped[str] = mapped_column(String(64), nullable=False)
    passport_issued_by: Mapped[str] = mapped_column(String(255), nullable=False)
    passport_issued_day: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    department_id: Mapped[int] = mapped_column(ForeignKey(
        "departments.id",
        ondelete="SET NULL"),
        nullable=True
    )
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="employees",
        foreign_keys=[department_id]
    )
    position: Mapped["Position"] = relationship(
        "Position",
        back_populates="employees"
    )
    work_times: Mapped[list["WorkTime"]] = relationship(
        back_populates="employee",
        cascade="all,delete-orphan"
    )
    vacations: Mapped[list["Vacation"]] = relationship(
        back_populates="employee",
        cascade="all,delete-orphan"

    )
    payrolls: Mapped[list["Payroll"]] = relationship(
        back_populates="employee",
        cascade="all,delete-orphan"
    )


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    code: Mapped[int] = mapped_column(unique=True, nullable=False)

    head_id: Mapped[int] = mapped_column(ForeignKey(
        "employees.id",
        ondelete="SET NULL"),
        nullable=True,
        unique=True
    )
    head: Mapped["Employee"] = relationship(
        "Employee",
        foreign_keys=[head_id],
        uselist=False
    )

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="department",
        foreign_keys=[Employee.department_id]
    )


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    hourly_rate: Mapped[float] = mapped_column(Float, nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="position"
    )


class WorkTime(Base):
    __tablename__ = "worktimes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    work_date: Mapped[date] = mapped_column(Date, nullable=False)
    hours_worked: Mapped[int] = mapped_column(default=0)
    is_weekend: Mapped[bool] = mapped_column(Boolean, default=False)
    is_holiday: Mapped[bool] = mapped_column(Boolean, default=False)

    employee: Mapped[Employee] = relationship(back_populates="work_times")


class Vacation(Base):
    __tablename__ = "vacations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_days: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(nullable=False)

    employee: Mapped[Employee] = relationship(back_populates="vacations")


class Payroll(Base):
    __tablename__ = "payrolls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    start_period: Mapped[date] = mapped_column(Date, nullable=False)
    end_period: Mapped[date] = mapped_column(Date, nullable=False)
    base_salary: Mapped[Decimal] = mapped_column(nullable=False)
    overtime_salary: Mapped[Decimal] = mapped_column(
        nullable=False,
        default=Decimal("0.0")
    )
    holiday_salary: Mapped[Decimal] = mapped_column(
        nullable=False,
        default=Decimal("0.0")
    )
    gross_salary: Mapped[Decimal] = mapped_column(nullable=False)
    net_salary: Mapped[Decimal] = mapped_column(nullable=False)
    tax: Mapped[Decimal] = mapped_column(nullable=False)
    penalty: Mapped[Decimal] = mapped_column(default=Decimal("0.0"))

    employee: Mapped[Employee] = relationship(back_populates="payrolls")
