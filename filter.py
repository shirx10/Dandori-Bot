from pipeline import extract_to_dataframe

# Filter by various fields: Class_ID, Course_Title, Instructor, Course_Type, Location, Cost, Skills, Description

folder = r"C:\Users\Andromeda\dflocal\dondari\myenv\data"
df_dondari = extract_to_dataframe(folder)

def filter_by(filter_class_id, filter_course_title, filter_instructor, filter_course_type, filter_location, df, query):
    """Filter dataframe by specified column and query string."""
    df_filtered = df
    
    if filter_class_id:
        df_filtered = df_filtered[df_filtered['Class_ID'].str.contains(query, case=False, na=False)]
    elif filter_course_title:
        df_filtered = df_filtered[df_filtered['Course_Title'].str.contains(query, case=False, na=False)]
    elif filter_instructor:
        df_filtered = df_filtered[df_filtered['Instructor'].str.contains(query, case=False, na=False)]
    elif filter_course_type:
        df_filtered = df_filtered[df_filtered['Course_Type'].str.contains(query, case=False, na=False)]
    elif filter_location:
        df_filtered = df_filtered[df_filtered['Location'].str.contains(query, case=False, na=False)]
    
    return df_filtered

result = filter_by(False, True, False, False, False, df_dondari, 'waffle')
print(result)