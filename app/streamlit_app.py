import streamlit as st

from data.programs import programs

from app.main import (
    normalize_field,
    normalize_degree,
    check_eligibility,
    validate_profile,
    calculate_match_score,
    get_match_level,
    get_improvement_suggestions
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

name = st.text_input(
    "👤 Name"
)


degree = st.selectbox(
    "🎓 Degree",
    [
        "B.Tech",
        "B.E",
        "B.Sc",
        "BCA"
    ]
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


country = st.selectbox(
    "🌍 Preferred Country",
    [
        "All Countries",
        "Germany",
        "France",
        "Ireland"
    ]
)


budget = st.number_input(
    "💰 Total Budget (INR)",
    min_value=1.0,
    value=1500000.0,
    step=50000.0
)


search = st.text_input(
    "🔎 Search Program or University",
    placeholder="e.g. Artificial Intelligence"
)


# -------------------------------
# Find Programs Button
# -------------------------------

if st.button("🔍 Find Suitable Programs"):

    if not name.strip():

        st.warning(
            "Please enter your name."
        )

    else:

        # -------------------------------
        # Student Profile
        # -------------------------------

        student = {

            "name": name,

            "degree": degree,

            "cgpa": cgpa,

            "ielts": ielts,

            "field": field,

            "country": country,

            "budget": budget

        }


        # -------------------------------
        # Validate Profile
        # -------------------------------

        if not validate_profile(student):

            st.error(
                "Invalid student profile."
            )

        else:

            # -------------------------------
            # Display Student Profile
            # -------------------------------

            st.subheader(
                "📋 Student Profile"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    "**Name:**",
                    name
                )

                st.write(
                    "**Degree:**",
                    degree
                )

                st.write(
                    "**CGPA:**",
                    cgpa
                )


            with col2:

                st.write(
                    "**IELTS:**",
                    ielts
                )

                st.write(
                    "**Field:**",
                    field
                )

                st.write(
                    "**Country:**",
                    country
                )

                st.write(
                    "**Budget:** ₹",
                    f"{budget:,.0f}"
                )


            st.divider()


            # -------------------------------
            # Program Results
            # -------------------------------

            st.subheader(
                "🎯 Program Results"
            )


            eligible_programs = []

            checked_programs = 0

            not_eligible_programs = 0


            # -------------------------------
            # Check Programs
            # -------------------------------

            for program in programs:

                # -------------------------------
                # Country Filter
                # -------------------------------

                if (
                    country != "All Countries"
                    and program["country"] != country
                ):

                    continue


                # -------------------------------
                # Search Filter
                # -------------------------------

                if search.strip():

                    search_text = (
                        search.strip().lower()
                    )


                    program_text = (

                        program["university"]
                        + " "
                        + program["course"]
                        + " "
                        + program["country"]

                    ).lower()


                    if search_text not in program_text:

                        continue


                # -------------------------------
                # Count Checked Programs
                # -------------------------------

                checked_programs += 1


                # -------------------------------
                # Eligibility Check
                # -------------------------------

                reasons, matched = check_eligibility(
                    student,
                    program
                )


                # -------------------------------
                # Eligible Program
                # -------------------------------

                if len(reasons) == 0:

                    eligible_programs.append(
                        program
                    )


                # -------------------------------
                # Not Eligible Program
                # -------------------------------

                else:

                    not_eligible_programs += 1


                    with st.expander(
                        f"❌ {program['course']} — "
                        f"{program['country']}"
                    ):

                        st.write(
                            "**Matched Criteria:**"
                        )


                        if len(matched) == 0:

                            st.write(
                                "None"
                            )

                        else:

                            for match in matched:

                                st.write(
                                    "✅",
                                    match
                                )


                        st.write(
                            "**Reasons:**"
                        )


                        for reason in reasons:

                            st.write(
                                "❌",
                                reason
                            )


                        # -------------------------------
                        # Improvement Suggestions
                        # -------------------------------

                        suggestions = (
                            get_improvement_suggestions(
                                student,
                                program
                            )
                        )


                        if len(suggestions) > 0:

                            st.write(
                                "💡 **How to Improve "
                                "Your Profile:**"
                            )


                            for suggestion in suggestions:

                                st.write(
                                    "👉",
                                    suggestion
                                )


            # -------------------------------
            # Eligibility Summary
            # -------------------------------

            st.divider()

            st.subheader(
                "📋 Eligibility Summary"
            )


            summary_col1, summary_col2, summary_col3 = (
                st.columns(3)
            )


            with summary_col1:

                st.metric(
                    "Programs Checked",
                    checked_programs
                )


            with summary_col2:

                st.metric(
                    "Eligible Programs",
                    len(eligible_programs)
                )


            with summary_col3:

                st.metric(
                    "Not Eligible",
                    not_eligible_programs
                )


            # -------------------------------
            # Sort Eligible Programs
            # -------------------------------

            eligible_programs.sort(
                key=lambda program:
                program["tuition_fee"]
            )


            # -------------------------------
            # Suitable Programs
            # -------------------------------

            if len(eligible_programs) > 0:

                st.divider()

                st.subheader(
                    "✅ Suitable Programs"
                )


                for program in eligible_programs:

                    reasons, matched = (
                        check_eligibility(
                            student,
                            program
                        )
                    )


                    # -------------------------------
                    # Match Score
                    # -------------------------------

                    match_score = (
                        calculate_match_score(
                            matched
                        )
                    )


                    # -------------------------------
                    # Match Level
                    # -------------------------------

                    match_level = (
                        get_match_level(
                            match_score
                        )
                    )


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
                        f"**Profile Match:** "
                        f"{match_score}%"
                    )


                    st.write(
                        f"**Admission Profile Level:** "
                        f"{match_level}"
                    )


                    # -------------------------------
                    # Profile Status
                    # -------------------------------

                    if match_score == 100:

                        st.success(
                            "🎉 Your profile meets all "
                            "currently checked requirements."
                        )

                    else:

                        suggestions = (
                            get_improvement_suggestions(
                                student,
                                program
                            )
                        )


                        if len(suggestions) > 0:

                            with st.expander(
                                "💡 How can you improve "
                                "your profile?"
                            ):

                                for suggestion in suggestions:

                                    st.write(
                                        "👉",
                                        suggestion
                                    )


                    # -------------------------------
                    # Score Breakdown
                    # -------------------------------

                    with st.expander(
                        "📊 View Score Breakdown"
                    ):

                        if (
                            "Degree matches the requirement."
                            in matched
                        ):

                            st.write(
                                "🎓 Degree: 20%"
                            )

                        else:

                            st.write(
                                "❌ Degree: 0%"
                            )


                        if (
                            "CGPA meets the requirement."
                            in matched
                        ):

                            st.write(
                                "📊 CGPA: 20%"
                            )

                        else:

                            st.write(
                                "❌ CGPA: 0%"
                            )


                        if (
                            "IELTS meets the requirement."
                            in matched
                        ):

                            st.write(
                                "📝 IELTS: 20%"
                            )

                        else:

                            st.write(
                                "❌ IELTS: 0%"
                            )


                        if (
                            "Field matches the program."
                            in matched
                        ):

                            st.write(
                                "💻 Field: 20%"
                            )

                        else:

                            st.write(
                                "❌ Field: 0%"
                            )


                        if (
                            "Budget is sufficient."
                            in matched
                        ):

                            st.write(
                                "💰 Budget: 20%"
                            )

                        else:

                            st.write(
                                "❌ Budget: 0%"
                            )


                    # -------------------------------
                    # Why Recommended
                    # -------------------------------

                    with st.expander(
                        "⭐ Why is this program recommended?"
                    ):

                        st.write(
                            "This program matches your "
                            "profile because:"
                        )


                        for match in matched:

                            st.write(
                                "✅",
                                match
                            )


                        st.write(
                            f"**Profile Match:** "
                            f"{match_score}%"
                        )


            else:

                st.warning(
                    "No suitable programs found "
                    "for the given filters and profile."
                )


            # -------------------------------
            # Most Affordable Option
            # -------------------------------

            if len(eligible_programs) > 0:

                st.divider()

                st.subheader(
                    "💰 Most Affordable Option"
                )


                cheapest_program = (
                    eligible_programs[0]
                )


                st.info(
                    f"🏆 {cheapest_program['course']} — "
                    f"{cheapest_program['country']}\n\n"
                    f"**University:** "
                    f"{cheapest_program['university']}\n\n"
                    f"**Tuition Fee:** "
                    f"₹{cheapest_program['tuition_fee']:,}"
                )


                # -------------------------------
                # Program Comparison
                # -------------------------------

                st.divider()

                st.subheader(
                    "📊 Program Comparison"
                )


                comparison_data = []


                for program in eligible_programs:

                    comparison_data.append({

                        "University":
                            program["university"],

                        "Country":
                            program["country"],

                        "Course":
                            program["course"],

                        "Tuition Fee":
                            f"₹{program['tuition_fee']:,}",

                        "Minimum CGPA":
                            program["minimum_cgpa"],

                        "Minimum IELTS":
                            program["minimum_ielts"],

                        "Language":
                            program["language"]

                    })


                st.dataframe(
                    comparison_data,
                    use_container_width=True
                )


                # -------------------------------
                # Recommended Programs
                # -------------------------------

                st.divider()

                st.subheader(
                    "⭐ Recommended Programs"
                )


                for program in eligible_programs:

                    st.info(
                        f"🌍 {program['country']} | "
                        f"{program['course']} | "
                        f"{program['university']}"
                    )