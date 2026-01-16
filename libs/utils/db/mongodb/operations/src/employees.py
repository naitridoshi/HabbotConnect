from datetime import datetime, timezone

import pymongo
from bson import ObjectId

from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.db.mongodb.operations.src.base import BaseOperations
from libs.utils.db.mongodb.src.repository import (
    employees_repository,
)
from libs.utils.enums.src import DepartmentType, RoleType

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
            {"is_active": True}
        )
        return self.create(employee_data)

    def list_employees(
        self, department: DepartmentType, role: RoleType, page: int, page_size: int
    ):
        query = {"is_active": True}
        if department:
            query["department"] = department.value
        if role:
            query["role"] = role.value

        total = self._repository.count_documents(query)
        skip = (page - 1) * page_size

        pipeline = [
            {"$match": query},
            {"$sort": {"date_joined": pymongo.DESCENDING}},
            {"$skip": skip},
            {"$limit": page_size},
        ]
        return list(self.repository.aggregate(pipeline)), total

    def get_employee_by_id(self, employee_id):
        return self.repository.find_one(
            {"_id": ObjectId(employee_id), "is_active": True}
        )

    def update_employee(self, employee_id: str, employee_data: dict):
        updated = self.repository.update_one(
            {"_id": ObjectId(employee_id), "is_active": True}, {"$set": employee_data}
        )
        if updated:
            return self.find_by_id(employee_id)
        return None

    def delete_employee(self, employee_id: str):
        return self.repository.update_one(
            {"_id": ObjectId(employee_id)}, {"$set": {"is_active": False}}
        )
