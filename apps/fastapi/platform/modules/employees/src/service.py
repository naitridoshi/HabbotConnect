from apps.fastapi.platform.modules.employees.src.dto import CreateEmployeeDTO
from libs.fastapi.platform.modules.employees.src import format_employee_record
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.common.responses.src import success_response
from libs.utils.db.mongodb.operations.src import (
    employees_operations,
)

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
            data={format_employee_record(employee_data, employee_id): employee_id},
            message="Employee created successfully",
        )

    @staticmethod
    @log.track
    def list_employees():
        employees_operations.list_employees()

        return success_response()


employee_service = EmployeeService()
