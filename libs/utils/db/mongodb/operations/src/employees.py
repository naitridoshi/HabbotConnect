from datetime import datetime, timezone

from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.db.mongodb.operations.src.base import BaseOperations
from libs.utils.db.mongodb.src.repository import (
    employees_repository,
)

log = CustomLogger("EmployeesOperations", is_request=False)
logger, listener = log.get_logger()
listener.start()


class EmployeesOperations(BaseOperations):
    def __init__(self):
        super().__init__(employees_repository)

    def get_employee_by_email(self, email):
        return self.repository.find_one({"email": email, "is_active": True})

    def create_employee(self, employee_data: dict):
        employee_data.update(
            {"is_active": True, "date_joined": datetime.now(timezone.utc)}
        )
        return self.repository.insert_one(employee_data)

    def list_employees(self):
        return self.repository.find({"is_active": True})
