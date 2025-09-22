from datetime import date

from sqlalchemy import ForeignKey, String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.engine import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    code: Mapped[int] = mapped_column(unique=True, nullable=False)
    head_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True, unique=True)
    head: Mapped["Employee"] = relationship(foreign_keys=[head_id], uselist=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    hourly_rate: Mapped[float] = mapped_column(nullable=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="position")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tab_number: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(64), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    passport_id: Mapped[str] = mapped_column(String(64), nullable=False)
    passport_issued_by: Mapped[str] = mapped_column(String(255), nullable=False)
    passport_issued_day: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))

    department: Mapped["Department"] = relationship(back_populates="employees")
    position: Mapped["Position"] = relationship(back_populates="employees")
