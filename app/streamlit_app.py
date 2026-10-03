import streamlit as st
from data.programs import programs
from app.main import (
    normalize_field,
    normalize_degree,
    check_eligibility,
    validate_profile
)


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Study Abroad Advisor",
    page_icon="🌍",
    layout="centered"
)


# -------------------------------
# Title
# -------------------------------

st.title("🌍 AI Study Abroad Advisor")

st.write(
    "Enter your academic profile, preferences and budget "
    "to find suitable study programs."
)


# -------------------------------
# Student Inputs
# -------------------------------

name = st.text_input("👤 Name")

degree = st.selectbox(
    "🎓 Degree",
    ["B.Tech", "B.E", "B.Sc", "BCA"]
)

cgpa = st.number_input(
    "📊 CGPA",
    min_value=0.0,
    max_value=10.0,
    value=7.0,
    step=0.1
)

ielts = st.number_input(
    "📝 IELTS Score",
    min_value=0.0,
    max_value=9.0,
    value=6.5,
    step=0.5
)

field = st.selectbox(
    "💻 Desired Field",
    [
        "Artificial Intelligence",
        "Data Science",
        "Computer Science"
    ]
)

budget = st.number_input(
    "💰 Total Budget (INR)",
    min_value=1.0,
    value=1500000.0,
    step=50000.0
)


# -------------------------------
# Find Programs Button
# -------------------------------

if st.button("🔍 Find Suitable Programs"):

    if not name.strip():

        st.warning("Please enter your name.")

    else:

        student = {
            "name": name,
            "degree": degree,
            "cgpa": cgpa,
            "ielts": ielts,
            "field": field,
            "budget": budget
        }

        if not validate_profile(student):

            st.error("Invalid student profile.")

        else:

            st.subheader("📋 Student Profile")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Name:**", name)
                st.write("**Degree:**", degree)
                st.write("**CGPA:**", cgpa)

            with col2:
                st.write("**IELTS:**", ielts)
                st.write("**Field:**", field)
                st.write("**Budget:** ₹", f"{budget:,.0f}")


            st.divider()

            st.subheader("🎯 Program Results")

            eligible_programs = []


            for program in programs:

                reasons, matched = check_eligibility(
                    student,
                    program
                )

                if len(reasons) == 0:

                    eligible_programs.append(program)

                    st.success(
                        f"✅ {program['course']} — "
                        f"{program['country']}"
                    )

                    st.write(
                        f"**University:** "
                        f"{program['university']}"
                    )

                    st.write(
                        f"**Tuition Fee:** "
                        f"₹{program['tuition_fee']:,}"
                    )

                    st.write(
                        f"**Language:** "
                        f"{program['language']}"
                    )

                    st.write(
                        f"**Match Score:** "
                        f"{len(matched)}/5"
                    )

                    with st.expander("View matched criteria"):

                        for match in matched:
                            st.write("✅", match)


                else:

                    with st.expander(
                        f"❌ {program['course']} — "
                        f"{program['country']}"
                    ):

                        st.write("**Matched Criteria:**")

                        for match in matched:
                            st.write("✅", match)

                        st.write("**Reasons:**")

                        for reason in reasons:
                            st.write("❌", reason)


            # -------------------------------
            # Recommendations
            # -------------------------------

            st.divider()

            st.subheader("⭐ Recommended Programs")

            if len(eligible_programs) == 0:

                st.warning(
                    "No suitable programs found "
                    "for the given profile."
                )

            else:

                for program in eligible_programs:

                    st.info(
                        f"🌍 {program['country']} | "
                        f"{program['course']} | "
                        f"{program['university']}"
                    )