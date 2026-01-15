from libs.utils.db.mongodb.operations.src.employees import EmployeesOperations
from libs.utils.db.mongodb.operations.src.users import UsersOperations

users_operations = UsersOperations()
employees_operations = EmployeesOperations()

__all__ = [
    "users_operations",
    "employees_operations",
]
