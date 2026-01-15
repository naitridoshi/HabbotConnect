def format_employee_record(employee_data, employee_id):
    return {
        "id": str(employee_id),
        "name": employee_data.get("name"),
        "email": employee_data.get("email"),
        "department": employee_data.get("department"),
        "role": employee_data.get("role"),
        "date_joined": employee_data.get("date_joined"),
    }


def format_employee_list_record(employee_list):
    employees = []
    for employee in employee_list:
        employees.append(format_employee_record(employee, employee.get))
