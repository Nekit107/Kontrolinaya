CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    position VARCHAR(50),
    salary int,
    hire_date DATE,
    department_id INT,
    CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget INT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(255),
    status task_status,
    project_id INT,
    assignee_id INT,
    CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id),
    CONSTRAINT fk_assignee FOREIGN KEY (assignee_id) REFERENCES employees(id)
);

CREATE TABLE employee_projects (
    employee_id INT,
    project_id INT ,
    role project_role,
    PRIMARY KEY (employee_id, project_id),
    CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(id),
    CONSTRAINT fk_project_assignment FOREIGN KEY (project_id) REFERENCES projects(id)
);
