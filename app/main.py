from data.programs import programs


# -------------------------------
# Text Normalization
# -------------------------------

def normalize_text(text):
    return text.strip().lower()


def normalize_field(field):

    field = normalize_text(field)

    if field in ["ai", "artificial intelligence", "a.i."]:
        return "ai"

    elif field in ["data science", "data scientist", "ds"]:
        return "data science"

    elif field in ["computer science", "cs"]:
        return "computer science"

    else:
        return field


def normalize_degree(degree):

    degree = normalize_text(degree)

    if degree in ["btech", "b.tech", "b.tech.", "b tech"]:
        return "btech"

    elif degree in ["be", "b.e", "b.e.", "bachelor of engineering"]:
        return "be"

    elif degree in ["bsc", "b.sc", "b.sc.", "bachelor of science"]:
        return "bsc"

    elif degree in ["bca", "b.c.a", "bachelor of computer applications"]:
        return "bca"

    else:
        return degree


# -------------------------------
# Student Profile
# -------------------------------

def get_student_profile():

    name = input("Enter your name: ").strip()
    degree = input("Enter your degree: ").strip()

    try:
        cgpa = float(input("Enter your CGPA: "))
    except ValueError:
        print("❌ Invalid CGPA. Please enter a number.")
        return None

    try:
        ielts = float(input("Enter your IELTS score: "))
    except ValueError:
        print("❌ Invalid IELTS score. Please enter a number.")
        return None

    field = input("Enter your desired field: ").strip()

    try:
        budget = float(input("Enter your total budget in INR: "))
    except ValueError:
        print("❌ Invalid budget. Please enter a number.")
        return None

    student = {
        "name": name,
        "degree": degree,
        "cgpa": cgpa,
        "ielts": ielts,
        "field": field,
        "budget": budget
    }

    return student


# -------------------------------
# Profile Validation
# -------------------------------

def validate_profile(student):

    if student["cgpa"] < 0 or student["cgpa"] > 10:
        print("❌ Invalid CGPA. CGPA must be between 0 and 10.")
        return False

    if student["ielts"] < 0 or student["ielts"] > 9:
        print("❌ Invalid IELTS score. IELTS must be between 0 and 9.")
        return False

    if student["budget"] <= 0:
        print("❌ Invalid budget. Budget must be greater than 0.")
        return False

    return True


# -------------------------------
# Eligibility Checking
# -------------------------------

def check_eligibility(student, program):

    reasons = []
    matched = []

    # CGPA
    if student["cgpa"] < program["minimum_cgpa"]:
        reasons.append("CGPA is below the minimum requirement.")
    else:
        matched.append("CGPA meets the requirement.")

    # Degree
    if normalize_degree(student["degree"]) != normalize_degree(
        program["required_degree"]
    ):
        reasons.append("Degree does not match the program requirement.")
    else:
        matched.append("Degree matches the requirement.")

    # IELTS
    if student["ielts"] < program["minimum_ielts"]:
        reasons.append("IELTS score is below the minimum requirement.")
    else:
        matched.append("IELTS meets the requirement.")

    # Field
    if normalize_field(student["field"]) != normalize_field(program["field"]):
        reasons.append("Field does not match the program.")
    else:
        matched.append("Field matches the program.")

    # Budget
    if student["budget"] < program["tuition_fee"]:
        reasons.append("Budget is lower than the tuition fee.")
    else:
        matched.append("Budget is sufficient.")

    return reasons, matched

def calculate_match_score(matched):

    score = len(matched) * 20

    return score

def get_match_level(score):

    if score >= 80:
        return "Strong Profile Match"

    elif score >= 60:
        return "Moderate Profile Match"

    elif score >= 40:
        return "Low Profile Match"

    else:
        return "Very Low Profile Match"