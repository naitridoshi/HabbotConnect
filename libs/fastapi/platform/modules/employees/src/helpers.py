def format_employee_record(employee_data, employee_id):
    return {
        "id": str(employee_id),
        "name": employee_data.get("name"),
        "email": employee_data.get("email"),
        "department": employee_data.get("department"),
        "role": employee_data.get("role"),
        "date_joined": employee_data.get("date_joined"),
    }


def format_employee_list_record(employee_list, total, page, page_size):
    employees = []

    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    for employee in employee_list:
        employees.append(format_employee_record(employee, employee.get("_id")))

    return {
        "total": total,
        "items": employees,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
