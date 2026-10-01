from data.programs import programs

def normalize_text(text):
    return text.strip().lower()

def get_student_profile():

    name = input("Enter your name: ")
    degree = input("Enter your degree: ").strip()
    cgpa = float(input("Enter your CGPA: "))
    ielts = float(input("Enter your IELTS score: "))
    field = input("Enter your desired field: ").strip()
    budget = float(input("Enter your total budget in INR: "))

    student = {
        "name": name,
        "degree": degree,
        "cgpa": cgpa,
        "ielts": ielts,
        "field": field,
        "budget": budget
    }

    return student


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


def check_eligibility(student, program):

    reasons = []

    if student["cgpa"] < program["minimum_cgpa"]:
        reasons.append("CGPA is below the minimum requirement.")

    if normalize_text(student["degree"]) != normalize_text(program["required_degree"]):
        reasons.append("Degree does not match the program requirement.")

    if student["ielts"] < program["minimum_ielts"]:
        reasons.append("IELTS score is below the minimum requirement.")

    if normalize_text(student["field"]) != normalize_text(program["field"]):
        reasons.append("Field does not match the program.")

    if student["budget"] < program["tuition_fee"]:
        reasons.append("Budget is lower than the tuition fee.")

    return reasons

student = get_student_profile()

if validate_profile(student):

    print("\n--- Student Profile ---")
    print(student)

    print("\n--- Program Eligibility ---")
    eligible_programs = []
    for program in programs:

        reasons = check_eligibility(student, program)

        print("\nUniversity:", program["university"])
        print("Country:", program["country"])
        print("Course:", program["course"])
        print("Tuition Fee:", program["tuition_fee"])

        if len(reasons) == 0:
            print("✅ Eligible")
            eligible_programs.append(program)
        else:
            print("❌ Not eligible")
            print("Reasons:")

            for reason in reasons:
                print("-", reason)

print("\n--- Recommended Programs ---")

if len(eligible_programs) == 0:
    print("❌ No suitable programs found.")

else:
    for program in eligible_programs:
        print("\nUniversity:", program["university"])
        print("Country:", program["country"])
        print("Course:", program["course"])
        print("Tuition Fee:", program["tuition_fee"])
        print("Language:", program["language"])
 