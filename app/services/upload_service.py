import csv
import io
from collections import defaultdict
from typing import Dict, List, Tuple

from app.repositories.student_repository import StudentRepository


def parse_csv(data: bytes) -> Tuple[Dict[str, List[int]], int, int]:
    text = data.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("CSV has no headers")
    actual_headers = [column.strip().lower() for column in reader.fieldnames]
    required_headers = {"full_name", "grade"}
    missing_headers = required_headers - set(actual_headers)
    if missing_headers:
        raise ValueError(f"Missing required columns: {', '.join(missing_headers)}")
    rows = list(reader)
    if not rows:
        raise ValueError("CSV is empty")
    student_grades: Dict[str, List[int]] = defaultdict(list)
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

        student_grades[name].append(grade)
    records = sum(len(grades) for grades in student_grades.values())
    students = len(student_grades)

    return student_grades, records, students
async def process_upload(repo:StudentRepository, csv_content: bytes)->Tuple[int, int]:
    student_grades, records_loaded, students_count = parse_csv(csv_content)
    student_names = list(student_grades.keys())
    name_to_id = await repo.insert_students(student_names)
    grade_records = []
    for name, grades in student_grades.items():
        student_id = name_to_id[name]
        for grade in grades:
            grade_records.append((student_id, grade))
    await repo.insert_grades(grade_records)
    return records_loaded, students_count