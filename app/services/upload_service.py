async def process_csv(data: bytes):
    text = data.decode('utf-8')
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ['full_name', 'grade']:
        raise ValueError("empty columns")
    rows = list(reader)
    if not rows:
        raise ValueError("CSV is empty")
    student_grades = {}
    for i, row in enumerate(rows, start=2):
        name = row.get('full_name', '').strip()
        grade_str = row.get('grade', '').strip()
        if not name:
            raise ValueError(f"Row {i}: empty full_name")
        if not grade_str:
            raise ValueError(f"Row {i}: empty grade")
        try:
            grade = int(grade_str)
        except ValueError:
            raise ValueError(f"Row {i}: grade must be integer")
        if grade < 2 or grade > 5:
            raise ValueError(f"Row {i}: grade must >= 2 and <=5")
        if name not in student_grades:
            student_grades[name] = []
        student_grades[name].append(grade)
    pool = await get_db()
    async with pool.acquire() as conn:
        async with conn.transaction():
            for name, grades in student_grades.items():
                row = await conn.fetchrow("SELECT id FROM students WHERE full_name = $1", name)
                if row:
                    student_id = row['id']
                else:
                    row = await conn.fetchrow("INSERT INTO students (full_name) VALUES ($1) RETURNING id", name)
                    student_id = row['id']
                for grade in grades:
                    await conn.execute("INSERT INTO grades (student_id, grade) VALUES ($1, $2)", student_id, grade)
    records = sum(len(grades) for grades in student_grades.values())
    students = len(student_grades)
    return records, students