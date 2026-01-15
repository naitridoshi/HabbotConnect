from apps.fastapi.platform.modules.employees.src.dto import CreateEmployeeDTO
from libs.fastapi.platform.modules.employees.src import format_employee_record
from libs.fastapi.platform.modules.employees.src.helpers import (
    format_employee_list_record,
)
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.common.responses.src import success_response
from libs.utils.db.mongodb.operations.src import (
    employees_operations,
)
from libs.utils.enums.src import DepartmentType, RoleType

log = CustomLogger("EmployeeService")
logger, listener = log.get_logger()
listener.start()


class EmployeeService:
    @staticmethod
    @log.track
    def create_employee(employee_data: CreateEmployeeDTO):
        existing_employee = employees_operations.get_employee_by_email(
            employee_data.email
        )

        if existing_employee:
            raise ValueError("Employee with email already exists")

        employee_id = employees_operations.create_employee(employee_data.model_dump())

        return success_response(
            data=format_employee_record(employee_data.model_dump(), employee_id),
            message="Employee created successfully",
        )

    @staticmethod
    @log.track
    def list_employees(
        department: DepartmentType, role: RoleType, page: int, page_size: int
    ):
        employees_list, total = employees_operations.list_employees(
            department, role, page, page_size
        )

        return success_response(
            data=format_employee_list_record(employees_list, total, page, page_size),
            message="Employees list fetched successfully",
        )

    @staticmethod
    @log.track
    def get_employee(employee_id: str):
        employee = employees_operations.get_employee_by_id(employee_id)

        if not employee:
            raise ValueError("Employee not found")

        return success_response(
            data=format_employee_record(employee, employee_id),
            message="Employee fetched successfully",
        )

    @staticmethod
    @log.track
    def update_employee(employee_id: str, updated_data: dict):
        employee = employees_operations.get_employee_by_id(employee_id)

        if not employee:
            raise ValueError("Employee not found")

        employee_updated = employees_operations.update_employee(
            employee_id, updated_data
        )

        if not employee_updated:
            raise ValueError("Error occurred in updating employee")

        return success_response(
            data=format_employee_record(employee_updated, employee_id),
            message="Employee updated successfully",
        )

    @staticmethod
    @log.track
    def delete_employee(employee_id: str):
        employee = employees_operations.get_employee_by_id(employee_id)

        if not employee:
            raise ValueError("Employee not found")

        employees_operations.delete_employee(employee_id)
        return None


employee_service = EmployeeService()
