

# -------------------------
# Simple validation helpers
# -------------------------
def is_valid_id(sid):
    # ID must not be empty and must not contain spaces
    return bool(sid) and (" " not in sid)

def is_valid_name(name):
    # Name must not be empty and should contain at least one letter
    return bool(name) and any(ch.isalpha() for ch in name)

def is_valid_age(age_str):
    # Age must be digits and > 0
    if not age_str:
        return False
    if not age_str.isdigit():
        return False
    return int(age_str) > 0

def is_valid_course(course):
    # Course should not be empty (simple check)
    return bool(course) and len(course.strip()) >= 2

def is_valid_email(email):
    # Very simple email check: has '@' and a dot after '@'
    if not email or " " in email:
        return False
    parts = email.split("@")
    return len(parts) == 2 and "." in parts[1]

# -------------------------
# Helper DB checks
# -------------------------
def student_exists(sid):
    q = "SELECT 1 FROM students WHERE id = %s;"
    rows = execute_query(q, (sid,), fetch=True)
    return bool(rows)

def email_exists(email, exclude_id=None):
    if exclude_id:
        q = "SELECT 1 FROM students WHERE email = %s AND id <> %s;"
        rows = execute_query(q, (email, exclude_id), fetch=True)
    else:
        q = "SELECT 1 FROM students WHERE email = %s;"
        rows = execute_query(q, (email,), fetch=True)
    return bool(rows)

# -------------------------
# CRUD functions
# -------------------------
def add_student(sid, name, age_str, course, email):
    # Basic validation
    if not is_valid_id(sid):
        return False, "Invalid ID: cannot be empty or contain spaces."
    if not is_valid_name(name):
        return False, "Invalid name."
    if not is_valid_age(age_str):
        return False, "Invalid age."
    if not is_valid_course(course):
        return False, "Invalid course."
    if not is_valid_email(email):
        return False, "Invalid email."

    if student_exists(sid):
        return False, "Student ID already exists."
    if email_exists(email):
        return False, "Email already in use."

    age = int(age_str)
    q = "INSERT INTO students (id, name, age, course, email) VALUES (%s, %s, %s, %s, %s);"
    try:
        execute_query(q, (sid, name.strip(), age, course.strip(), email.strip()))
        return True, "Student added."
    except RuntimeError as e:
        return False, f"DB error: {e}"

def remove_student(sid):
    if not is_valid_id(sid):
        return False, "Invalid ID."
    if not student_exists(sid):
        return False, "No such student."

    q = "DELETE FROM students WHERE id = %s;"
    try:
        execute_query(q, (sid,))
        return True, "Student removed."
    except RuntimeError as e:
        return False, f"DB error: {e}"

def update_student(sid, name=None, age_str=None, course=None, email=None):
    if not is_valid_id(sid):
        return False, "Invalid ID."
    if not student_exists(sid):
        return False, "No such student."

    fields = []
    params = []

    if name is not None:
        if not is_valid_name(name):
            return False, "Invalid name."
        fields.append("name = %s")
        params.append(name.strip())

    if age_str is not None:
        if not is_valid_age(age_str):
            return False, "Invalid age."
        fields.append("age = %s")
        params.append(int(age_str))

    if course is not None:
        if not is_valid_course(course):
            return False, "Invalid course."
        fields.append("course = %s")
        params.append(course.strip())

    if email is not None:
        if not is_valid_email(email):
            return False, "Invalid email."
        if email_exists(email, exclude_id=sid):
            return False, "Email used by another student."
        fields.append("email = %s")
        params.append(email.strip())

    if not fields:
        return False, "No fields to update."

    params.append(sid)
    set_clause = ", ".join(fields)
    q = f"UPDATE students SET {set_clause} WHERE id = %s;"
    try:
        execute_query(q, tuple(params))
        return True, "Student updated."
    except RuntimeError as e:
        return False, f"DB error: {e}"

def search_students(keyword):
    # Simple search on id, name or course (case-insensitive)
    kw = f"%{keyword}%"
    q = """
    SELECT id, name, age, course, email
    FROM students
    WHERE id ILIKE %s OR name ILIKE %s OR course ILIKE %s
    ORDER BY id;
    """
    try:
        rows = execute_query(q, (kw, kw, kw), fetch=True)
        return True, rows
    except RuntimeError as e:
        return False, f"DB error: {e}"

def list_all_students():
    q = "SELECT id, name, age, course, email FROM students ORDER BY id;"
    try:
        rows = execute_query(q, fetch=True)
        return True, rows
    except RuntimeError as e:
        return False, f"DB error: {e}"
