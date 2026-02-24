import fitz
import os
import pandas as pd  
import re  

def extract_to_dataframe(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    all_data = []
    
    print(f"Found {len(pdf_files)} files. Starting extraction...\n")

    for filename in pdf_files:
        file_path = os.path.join(folder_path, filename)

        try:
            doc = fitz.open(file_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()

            # Remove '.pdf'
            name_no_ext = filename.lower().replace('.pdf', '')
            parts = name_no_ext.split('_')
            course_title = " ".join(parts[2:]).title()

            id_match = re.search(r"Class ID:\s*(CLASS_\d+)", full_text, re.IGNORECASE)
            instr_match = re.search(r"Instructor:\s*\n*(.*?)\n", full_text, re.IGNORECASE)
            type_match = re.search(r"Course Type:\s*\n*(.*?)\n", full_text, re.IGNORECASE)
            loc_match = re.search(r"Location:\s*\n*(.*?)\n", full_text, re.IGNORECASE)
            cost_match = re.search(r"Cost:\s*\n*(£?\d+\.?\d*)", full_text, re.IGNORECASE)

            skl_match = re.search(r"Skills Developed\n(.*?)\n(?=Course Description)", full_text, re.DOTALL)
            desc_match = re.search(r"Course Description\n(.*?)\n(?=Class ID:)", full_text, re.DOTALL)

            all_data.append({
                "Filename": filename,
                "Class_ID": id_match.group(1).strip() if id_match else "Not Found",
                "Course_Title": course_title,
                "Instructor": instr_match.group(1).strip() if instr_match else "Unknown",
                "Course_Type": type_match.group(1).strip() if type_match else "Unknown",
                "Location": loc_match.group(1).strip() if loc_match else "Unknown",
                "Cost": cost_match.group(1).strip() if cost_match else "Unknown",
                "Skills": skl_match.group(1).strip().replace('\n', ', ') if skl_match else "Unknown",
                "Description": desc_match.group(1).strip() if desc_match else "Unknown"
            })

        except Exception as e:
            print(f"Could not read {filename}: {e}")

    return all_data

#folder = r"./courses"
#df_dandori = extract_to_dataframe(folder)

#print("\n--- Final Structured Dandori Data ---")
#if not df_dandori.empty:
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', 1000)
    #print(df_dandori[['Class_ID', 'Course_Title', 'Instructor', 'Cost']].head())
#else:
    #print("No data extracted. Check your folder path.")