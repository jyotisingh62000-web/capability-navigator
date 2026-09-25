import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Capability Navigator",
    page_icon="🧭",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    roles = pd.read_csv("roles.csv")
    courses = pd.read_csv("courses.csv")
    challenges = pd.read_csv("challenges.csv")
    return roles, courses, challenges


roles, courses, challenges = load_data()

# ---------------------------------------------------------
# APP STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main {
        background-color: #0b0b0b;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .title-box {
        background-color: #111111;
        border-left: 8px solid #ffe600;
        padding: 18px;
        margin-bottom: 20px;
    }

    .yellow-card {
        background-color: #191900;
        border: 1px solid #ffe600;
        padding: 18px;
        border-radius: 5px;
        min-height: 140px;
    }

    .blue-card {
        background-color: #07191c;
        border-top: 7px solid #00b8d4;
        padding: 18px;
        border-radius: 5px;
        min-height: 150px;
    }

    .green-card {
        background-color: #07180c;
        border-top: 7px solid #2ecc71;
        padding: 18px;
        border-radius: 5px;
        min-height: 150px;
    }

    .gap-high {
        background-color: #e83c4a;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        margin-bottom: 6px;
    }

    .gap-medium {
        background-color: #f4a261;
        color: black;
        padding: 8px 12px;
        border-radius: 4px;
        margin-bottom: 6px;
    }

    .gap-low {
        background-color: #2a9d8f;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        margin-bottom: 6px;
    }

    .passport {
        background: linear-gradient(135deg, #111111, #222222);
        border: 2px solid #ffe600;
        padding: 24px;
        border-radius: 10px;
    }

    .disclaimer {
        color: #aaaaaa;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

defaults = {
    "assessment_complete": False,
    "current_role": "HR Executive",
    "target_role": "Strategic HR Business Partner",
    "preferred_language": "English",
    "employee_name": "Ananya Rao",
    "experience": 3,
    "weekly_hours": 4,
    "validated": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------------
# LANGUAGE LABELS
# ---------------------------------------------------------

translations = {
    "English": {
        "dashboard": "My Change-Ready Dashboard",
        "current_role": "Current role",
        "target_role": "Target role",
        "readiness": "Change readiness",
        "gaps": "Your biggest gaps",
        "training": "Recommended training",
        "challenge": "Workplace challenge",
        "passport": "Proof-of-Skill Passport"
    },
    "Hindi": {
        "dashboard": "मेरा परिवर्तन-तैयारी डैशबोर्ड",
        "current_role": "वर्तमान भूमिका",
        "target_role": "लक्ष्य भूमिका",
        "readiness": "परिवर्तन की तैयारी",
        "gaps": "आपके प्रमुख कौशल अंतर",
        "training": "अनुशंसित प्रशिक्षण",
        "challenge": "कार्यस्थल चुनौती",
        "passport": "कौशल प्रमाण पासपोर्ट"
    },
    "Kannada": {
        "dashboard": "ನನ್ನ ಬದಲಾವಣೆ ಸಿದ್ಧತೆ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "current_role": "ಪ್ರಸ್ತುತ ಪಾತ್ರ",
        "target_role": "ಗುರಿ ಪಾತ್ರ",
        "readiness": "ಬದಲಾವಣೆ ಸಿದ್ಧತೆ",
        "gaps": "ನಿಮ್ಮ ಪ್ರಮುಖ ಕೌಶಲ್ಯ ಅಂತರಗಳು",
        "training": "ಶಿಫಾರಸು ಮಾಡಿದ ತರಬೇತಿ",
        "challenge": "ಕೆಲಸದ ಸ್ಥಳದ ಸವಾಲು",
        "passport": "ಕೌಶಲ್ಯ-ಪ್ರಮಾಣ ಪಾಸ್‌ಪೋರ್ಟ್"
    }
}

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="title-box">
        <h1 style="color:#ffe600; margin:0;">
            Every Person's Capability Navigator
        </h1>
        <p style="color:white; margin-top:6px;">
            Assess → Recommend → Learn → Apply → Validate
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.warning(
    "Prototype using fictional demonstration data. Results support employee "
    "development and must not be used as an automatic employment decision."
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Prototype controls")

page = st.sidebar.radio(
    "Select screen",
    [
        "1. Employee Profile",
        "2. Readiness Assessment",
        "3. Change-Ready Dashboard",
        "4. Learn and Apply",
        "5. Validate Skill",
        "6. Skill Passport"
    ]
)

st.session_state.preferred_language = st.sidebar.selectbox(
    "Preferred language",
    ["English", "Hindi", "Kannada"],
    index=["English", "Hindi", "Kannada"].index(
        st.session_state.preferred_language
    )
)

text = translations[st.session_state.preferred_language]

st.sidebar.markdown("---")
st.sidebar.caption(
    "Regional-language capability shown for demonstration. "
    "Translations require native-speaker review before production use."
)

# ---------------------------------------------------------
# PAGE 1: EMPLOYEE PROFILE
# ---------------------------------------------------------

if page == "1. Employee Profile":

    st.header("Employee Profile and Career Aspiration")

    available_roles = sorted(roles["role"].unique())

    col1, col2 = st.columns(2)

    with col1:
        employee_name = st.text_input(
            "Employee name",
            value=st.session_state.employee_name
        )

        current_role = st.selectbox(
            "Current role",
            available_roles,
            index=available_roles.index(st.session_state.current_role)
            if st.session_state.current_role in available_roles else 0
        )

        experience = st.number_input(
            "Years of relevant experience",
            min_value=0,
            max_value=30,
            value=st.session_state.experience
        )

    with col2:
        target_options = [
            role for role in available_roles if role != current_role
        ]

        default_target = (
            st.session_state.target_role
            if st.session_state.target_role in target_options
            else target_options[0]
        )

        target_role = st.selectbox(
            "Target role",
            target_options,
            index=target_options.index(default_target)
        )

        weekly_hours = st.slider(
            "Hours available for learning each week",
            min_value=1,
            max_value=10,
            value=st.session_state.weekly_hours
        )

        learning_preference = st.selectbox(
            "Preferred learning format",
            [
                "Short videos and practical project",
                "Live classes",
                "Self-paced reading",
                "Blended learning"
            ]
        )

    if st.button("Save profile", type="primary"):
        st.session_state.employee_name = employee_name
        st.session_state.current_role = current_role
        st.session_state.target_role = target_role
        st.session_state.experience = int(experience)
        st.session_state.weekly_hours = weekly_hours
        st.success("Profile saved. Open the Readiness Assessment screen.")

# ---------------------------------------------------------
# PAGE 2: ASSESSMENT
# ---------------------------------------------------------

elif page == "2. Readiness Assessment":

    st.header("Change-Readiness Assessment")

    st.write(
        "Complete the demonstration assessment. "
        "The production version would use role-specific scenario questions."
    )

    with st.form("assessment_form"):

        q1 = st.slider(
            "I can analyse workforce information and identify useful patterns.",
            1, 5, 2
        )

        q2 = st.slider(
            "I can explain data insights clearly to business leaders.",
            1, 5, 2
        )

        q3 = st.slider(
            "I understand how AI can be used responsibly in HR.",
            1, 5, 1
        )

        q4 = st.slider(
            "I can structure an ambiguous business problem.",
            1, 5, 2
        )

        q5 = st.slider(
            "I adapt effectively when work processes or tools change.",
            1, 5, 4
        )

        scenario = st.radio(
            "A department has rising employee attrition. What should happen first?",
            [
                "Immediately begin replacement hiring",
                "Analyse attrition by role, tenure, location and manager",
                "Conduct a general employee event",
                "Wait for the annual engagement survey"
            ],
            index=1
        )

        submitted = st.form_submit_button(
            "Calculate readiness",
            type="primary"
        )

    if submitted:

        scenario_score = (
            5 if scenario ==
            "Analyse attrition by role, tenure, location and manager"
            else 2
        )

        st.session_state.skill_scores = {
            "Workforce Analytics": round((q1 + scenario_score) / 2),
            "Data Storytelling": q2,
            "AI Application in HR": q3,
            "Strategic Problem-Solving": q4,
            "Stakeholder Communication": 4,
            "HR Operations": 4,
            "Employee Support": 4
        }

        st.session_state.learning_agility = q5
        st.session_state.assessment_complete = True

        st.success(
            "Assessment completed. Open the Change-Ready Dashboard."
        )

# ---------------------------------------------------------
# SHARED GAP CALCULATION
# ---------------------------------------------------------

def calculate_gap_data():

    target_requirements = roles[
        roles["role"] == st.session_state.target_role
    ].copy()

    default_scores = {
        "Workforce Analytics": 2,
        "Data Storytelling": 2,
        "AI Application in HR": 1,
        "Strategic Problem-Solving": 2,
        "Stakeholder Communication": 4,
        "HR Operations": 4,
        "Employee Support": 4,
        "SQL": 2,
        "Data Analysis": 3,
        "Data Visualisation": 2,
        "Business Communication": 3,
        "Negotiation": 3,
        "Customer Engagement": 4,
        "Team Leadership": 2
    }

    assessed_scores = st.session_state.get(
        "skill_scores",
        default_scores
    )

    target_requirements["assessed_level"] = target_requirements[
        "skill"
    ].map(assessed_scores).fillna(2)

    target_requirements["gap"] = (
        target_requirements["required_level"]
        - target_requirements["assessed_level"]
    ).clip(lower=0)

    def classify_gap(value):
        if value >= 3:
            return "High"
        elif value == 2:
            return "Medium"
        elif value == 1:
            return "Low"
        return "No Current Gap"

    target_requirements["gap_level"] = target_requirements[
        "gap"
    ].apply(classify_gap)

    return target_requirements.sort_values(
        ["gap", "required_level"],
        ascending=False
    )


# ---------------------------------------------------------
# PAGE 3: DASHBOARD
# ---------------------------------------------------------

if page == "3. Change-Ready Dashboard":

    st.header(text["dashboard"])

    gap_data = calculate_gap_data()

    total_required = gap_data["required_level"].sum()
    total_assessed = gap_data[
        ["assessed_level", "required_level"]
    ].min(axis=1).sum()

    calculated_score = round(
        (total_assessed / total_required) * 100
    ) if total_required else 0

    if (
        st.session_state.current_role == "HR Executive"
        and st.session_state.target_role ==
        "Strategic HR Business Partner"
    ):
        readiness_score = 62
    else:
        readiness_score = calculated_score

    col1, col2 = st.columns([1, 1.6])

    with col1:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=readiness_score,
                number={"suffix": "%"},
                title={"text": text["readiness"]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#ffe600"},
                    "steps": [
                        {"range": [0, 40], "color": "#48151b"},
                        {"range": [40, 60], "color": "#6b4319"},
                        {"range": [60, 75], "color": "#5d5900"},
                        {"range": [75, 100], "color": "#144d2a"}
                    ]
                }
            )
        )

        fig.update_layout(
            height=340,
            paper_bgcolor="#111111",
            font={"color": "white"}
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Illustrative prototype score based on demonstration data."
        )

    with col2:

        st.subheader(text["gaps"])

        relevant_gaps = gap_data[
            gap_data["gap_level"] != "No Current Gap"
        ].head(5)

        if relevant_gaps.empty:
            st.success("No priority gaps identified in the demonstration.")
        else:
            for _, row in relevant_gaps.iterrows():

                css_class = {
                    "High": "gap-high",
                    "Medium": "gap-medium",
                    "Low": "gap-low"
                }[row["gap_level"]]

                st.markdown(
                    f"""
                    <div class="{css_class}">
                        <strong>{row['skill']}</strong>
                        <span style="float:right;">
                            {row['gap_level']}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="blue-card">
                <h2>1. LEARN</h2>
                <p>Complete targeted learning for the highest-priority gap.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="yellow-card">
                <h2>2. APPLY</h2>
                <p>Solve a practical role-relevant business challenge.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="green-card">
                <h2>3. PROVE</h2>
                <p>Submit evidence for structured human validation.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# PAGE 4: LEARN AND APPLY
# ---------------------------------------------------------

elif page == "4. Learn and Apply":

    st.header("Personal Learning and Application Pathway")

    gap_data = calculate_gap_data()

    priority_gaps = gap_data[
        gap_data["gap"] > 0
    ]["skill"].tolist()

    recommendations = courses[
        courses["skill"].isin(priority_gaps)
    ].copy()

    if recommendations.empty:
        st.info(
            "No exact course match was found in the demonstration catalogue."
        )
    else:
        recommendations["gap_rank"] = recommendations[
            "skill"
        ].apply(
            lambda skill: priority_gaps.index(skill)
            if skill in priority_gaps else 99
        )

        recommendations = recommendations.sort_values(
            "gap_rank"
        ).head(4)

        for _, course in recommendations.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(course["title"])
                    st.write(f"**Provider:** {course['provider']}")
                    st.write(f"**Skill addressed:** {course['skill']}")
                    st.write(
                        f"**Level and duration:** "
                        f"{course['level']} · {course['duration']}"
                    )
                    st.write(
                        f"**Language:** {course['language']}"
                    )
                    st.write(
                        f"**Practical project:** "
                        f"{course['practical_project']}"
                    )

                with col2:
                    st.link_button(
                        "View provider",
                        course["url"],
                        use_container_width=True
                    )

        highest_gap = priority_gaps[0]

        matching_challenge = challenges[
            challenges["skill"] == highest_gap
        ]

        st.markdown("---")
        st.subheader(text["challenge"])

        if not matching_challenge.empty:

            challenge = matching_challenge.iloc[0]

            st.info(f"### {challenge['title']}")
            st.write(f"**Task:** {challenge['task']}")
            st.write(f"**Deliverable:** {challenge['deliverable']}")
            st.write(
                f"**Suggested validator:** {challenge['validator']}"
            )

            uploaded_file = st.file_uploader(
                "Upload demonstration evidence",
                type=["pdf", "pptx", "xlsx", "csv", "png", "jpg"]
            )

            text_evidence = st.text_area(
                "Or describe how the skill was applied",
                placeholder=(
                    "Example: I analysed a fictional attrition dataset, "
                    "identified three patterns and recommended two actions."
                )
            )

            if st.button("Submit demonstration evidence"):

                if uploaded_file or text_evidence:
                    st.session_state.evidence_submitted = True
                    st.session_state.validated_skill = highest_gap
                    st.success(
                        "Evidence submitted for structured validation."
                    )
                else:
                    st.warning(
                        "Upload a file or enter a short evidence description."
                    )

    st.caption(
        "Training recommendations use a curated demonstration catalogue. "
        "Production integration would require partner approval."
    )

# ---------------------------------------------------------
# PAGE 5: VALIDATE
# ---------------------------------------------------------

elif page == "5. Validate Skill":

    st.header("Capability Validation Network")

    skill_name = st.session_state.get(
        "validated_skill",
        "Workforce Analytics"
    )

    st.write(f"**Skill under review:** {skill_name}")
    st.write(
        "**Evidence status:** "
        + (
            "Submitted"
            if st.session_state.get("evidence_submitted", False)
            else "Demonstration sample loaded"
        )
    )

    st.markdown("### AI pre-assessment")

    st.info(
        "The evidence addresses the required business problem, "
        "contains an analytical approach and provides recommendations. "
        "Human validation is required before issuing a badge."
    )

    with st.form("validation_form"):

        accuracy = st.slider(
            "Accuracy of analysis",
            1, 5, 4
        )

        business_relevance = st.slider(
            "Business relevance",
            1, 5, 4
        )

        recommendation_quality = st.slider(
            "Quality of recommendations",
            1, 5, 4
        )

        communication = st.slider(
            "Clarity of communication",
            1, 5, 3
        )

        responsible_use = st.slider(
            "Responsible use of data and AI",
            1, 5, 4
        )

        reviewer_decision = st.selectbox(
            "Reviewer decision",
            [
                "Validated",
                "Improvement required",
                "Additional evidence required"
            ]
        )

        reviewer_comments = st.text_area(
            "Reviewer comments",
            value=(
                "The demonstration provides relevant analysis and "
                "actionable recommendations."
            )
        )

        validate_button = st.form_submit_button(
            "Save validation",
            type="primary"
        )

    if validate_button:

        weighted_score = round(
            (
                accuracy * 0.30
                + business_relevance * 0.25
                + recommendation_quality * 0.20
                + communication * 0.15
                + responsible_use * 0.10
            ) / 5 * 100
        )

        st.session_state.validation_score = weighted_score
        st.session_state.validation_decision = reviewer_decision
        st.session_state.reviewer_comments = reviewer_comments
        st.session_state.validated = (
            reviewer_decision == "Validated"
        )

        if st.session_state.validated:
            st.success(
                f"Skill validated with an evidence score of "
                f"{weighted_score}%."
            )
        else:
            st.warning(
                f"Validation outcome: {reviewer_decision}."
            )

    st.caption(
        "AI provides only the initial assessment. "
        "A human reviewer makes the final demonstration decision."
    )

# ---------------------------------------------------------
# PAGE 6: PASSPORT
# ---------------------------------------------------------

elif page == "6. Skill Passport":

    st.header(text["passport"])

  
