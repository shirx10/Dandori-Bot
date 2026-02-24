import os
import streamlit as st
import pandas as pd
from map import map_image
from google.cloud import firestore

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/secrets/GOOGLE_APPLICATION_CREDENTIALS"
db = firestore.Client()


@st.cache_data 
def get_all_courses():
    docs = db.collection("courses").stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])

@st.cache_data
def skills_set(df):
    return set(df['Skills'].str.split(',').explode().str.strip())

st.session_state.df_dandori = get_all_courses()
skills = skills_set(st.session_state.df_dandori)
display_cols = [
    'Class_ID',
    'Course_Title',
    'Instructor',
    'Location',
    'Course_Type',
    'Cost'
]

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = st.session_state.df_dandori.copy()

if "title_query" not in st.session_state:
    st.session_state.title_query = ""

def apply_filters():
    df = st.session_state.df_dandori.copy()

    if st.session_state.course_type != "All":
        df = df[df['Course_Type'] == st.session_state.course_type]

    if st.session_state.skills_search:
        df = df[df['Skills'].str.split(',').apply(
            lambda x: any(skill.strip() in st.session_state.skills_search for skill in x)
        )]

    if st.session_state.location_search != "All":
        df = df[df['Location'] == st.session_state.location_search]

    if st.session_state.title_query:
        df = df[df['Course_Title'].str.contains(
            st.session_state.title_query, case=False, na=False
        )]

    if st.session_state.cost_filter:
        df = df[df['Cost'].str.replace('£', '').astype(float) <= st.session_state.cost_filter]

    st.session_state.filtered_df = df


st.sidebar.header("Search Courses")

st.sidebar.selectbox(
    "Filter by Course Type",
    options=["All"] + sorted(st.session_state.df_dandori['Course_Type'].unique().tolist()),
    key="course_type",
    on_change=apply_filters
)

st.sidebar.selectbox(
    "Search by Location",
    options=["All"] + sorted(st.session_state.df_dandori['Location'].unique().tolist()),
    key="location_search",
    on_change=apply_filters
)

st.sidebar.multiselect(
    "Search by skills",
    options=sorted(skills),
    key="skills_search",
    on_change=apply_filters
)

st.sidebar.slider(
    "Maximum Cost (£)",
    min_value=0,
    max_value=int(st.session_state.df_dandori['Cost'].str.replace('£', '').astype(float).max()),
    step=10,
    key="cost_filter",
    on_change=apply_filters
)

st.sidebar.text_input(
    "Search by Course Title:",
    key="title_query",
    on_change=apply_filters
)

filtered_df = st.session_state.filtered_df

st.title("School of Dandori Course Catalog")
  

st.subheader("Extracted Course Data", text_alignment="center")
if not filtered_df.empty:
    event = st.dataframe(
    filtered_df[display_cols],
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun"
    )

    if event.selection.rows:
        selected_index = event.selection.rows[0]
        course = filtered_df.iloc[selected_index]

        st.divider()
        st.subheader(course["Course_Title"])

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Instructor:** {course['Instructor']}")
            st.write(f"**Location:** {course['Location']}")
            st.write(f"**Course Type:** {course['Course_Type']}")
        with col2:
            st.write(f"**Cost:** {course['Cost']}")
            st.write(f"**Skills:** {course['Skills']}")

        st.markdown("### Course Description")
        st.write(course["Description"])
    else:
        st.info("Click a course above to view full details.")
