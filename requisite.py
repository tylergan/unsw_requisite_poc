import logging
from model import Query, Student, Course

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def process(query: Query, student: Student) -> bool:
    course = Course(query)
    logging.info(f"{course}, {student}")
    return course.evaluate_requisites(student)


if __name__ == "__main__":
    # (expresison, completed_courses, expected)
    test_cases = [
        (
            Query("XYZW3331: (ABCD2521 or EFGH2611) and IJKL3311"), 
            Student({'ABCD2521', 'IJKL3311'}, 12), 
            True
        ),
        (
            Query("COMP3311: (COMP2521 or COMP1531) and COMP3331"),
            Student({'COMP2521', 'COMP3331'}, 12),
            True
        ),
        (
            Query("FINS1612: FINS1511 and not FINS1613"),
            Student({'FINS1511', 'FINS1613'}, 12),
            False
        ),
        (
            Query("GEND1234: at least 12UOC"),
            Student({'ABCD2521', 'IJKL3311'}, 12),
            True
        ),
        (
            Query("GEND1234: greater than 12UOC"),
            Student({'ABCD2521', 'IJKL3311'}, 12),
            False
        ),
        (
            Query("GEND1234: less than 12UOC"),
            Student({'ABCD2521', 'IJKL3311'}, 12),
            False
        ),
        (
            Query("GEND1234: at least 12UOC"),
            Student({'ABCD2521', 'IJKL3311'}, 6),
            False
        ),
    ]
    for i, (query, completed_courses, expected) in enumerate(test_cases):
        assert process(query, completed_courses) == expected
        print(f"\nTest {i+1} PASSED\n")
