def test_employees_requires_auth(client):
    response = client.get("/api/employees")

    assert response.status_code == 403


def test_employees_list_with_override(app, client, monkeypatch):
    from apps.fastapi.auth.src.helpers import require_user
    from apps.fastapi.platform.modules.employees.src import service as employee_service

    def fake_list_employees(_department, _role, _page, _page_size):
        return {
            "success": True,
            "message": "Employees list fetched successfully",
            "data": {
                "items": [],
                "total": 0,
                "page": 1,
                "pageSize": 10,
                "totalPages": 0,
            },
        }

    app.dependency_overrides[require_user] = lambda: {"email": "tester@example.com"}
    monkeypatch.setattr(
        employee_service.employee_service, "list_employees", fake_list_employees
    )

    response = client.get("/api/employees?page=1&page_size=10")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["items"] == []


def test_employees_create_with_override(app, client, monkeypatch):
    from apps.fastapi.auth.src.helpers import require_user
    from apps.fastapi.platform.modules.employees.src import service as employee_service

    def fake_create_employee(_employee_data):
        return {
            "success": True,
            "message": "Employee created successfully",
            "data": {
                "id": "emp-123",
                "name": "Alice",
                "email": "alice@example.com",
                "department": "HR",
                "role": "MANAGER",
                "date_joined": "2025-01-01T00:00:00Z",
            },
        }

    app.dependency_overrides[require_user] = lambda: {"email": "tester@example.com"}
    monkeypatch.setattr(
        employee_service.employee_service, "create_employee", fake_create_employee
    )

    response = client.post(
        "/api/employees",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "department": "HR",
            "role": "MANAGER",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["data"]["id"] == "emp-123"


def test_employees_update_with_override(app, client, monkeypatch):
    from apps.fastapi.auth.src.helpers import require_user
    from apps.fastapi.platform.modules.employees.src import service as employee_service

    def fake_update_employee(_employee_id, _updated_data):
        return {
            "success": True,
            "message": "Employee updated successfully",
            "data": {
                "id": "emp-123",
                "name": "Alice Updated",
                "email": "alice@example.com",
                "department": "HR",
                "role": "MANAGER",
                "date_joined": "2025-01-01T00:00:00Z",
            },
        }

    app.dependency_overrides[require_user] = lambda: {"email": "tester@example.com"}
    monkeypatch.setattr(
        employee_service.employee_service, "update_employee", fake_update_employee
    )

    response = client.put(
        "/api/employees/emp-123",
        json={"name": "Alice Updated"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["name"] == "Alice Updated"


def test_employees_delete_with_override(app, client, monkeypatch):
    from apps.fastapi.auth.src.helpers import require_user
    from apps.fastapi.platform.modules.employees.src import service as employee_service

    def fake_delete_employee(_employee_id):
        return None

    app.dependency_overrides[require_user] = lambda: {"email": "tester@example.com"}
    monkeypatch.setattr(
        employee_service.employee_service, "delete_employee", fake_delete_employee
    )

    response = client.delete("/api/employees/emp-123")

    assert response.status_code == 204
