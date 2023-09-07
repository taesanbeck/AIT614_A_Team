import streamlit as st


def show_page():
    # Team photo
    st.image("streamlit_modules/media/team_photo.PNG")
    
    # Formatting Center Align
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="centered">', unsafe_allow_html=True) # Center align columns

    col1, col2, col3, col4, col5, col6 = st.columns(6)  # Define col1 to col6 using columns

    with col1:
        st.subheader('Michelle')
        st.write('''My name is Michelle, pronounced "mi-SHELL-ee".

- Born in Brasil.
- Former Research Coordinator at the University of Florida, focusing on summary statistics, grant writing, and workshops.
- ORISE fellow at FDA's Office of Analytics and Outreach, creating R Shiny applications for data simulation.
- Proficient in R, R Shiny, and Python.''')




    with col2:
        st.subheader('Prakriti')
        st.write('''My name is Prakriti P Panday. 
- Pursuing a PhD in computational bio and bioinformatics at GMU.
- Proficient in SQL, Python, and R, with exposure to NLP and machine learning algorithms.
- Experienced as a Teacher's Assistant for the NLP course, assisting students with queries and database concepts.
''')

    with col3:
        st.subheader('Amy')
        st.write('''Hi, my name is Amy Vaughan. 
- DAEN master's student in Applied Analytics.
- Graduated from Reed College with a bachelor's in linguistics.
- Experienced analyst in the civil service.
- Self-taught Python programmer and database admin for a decade.
- Enjoy coding chat bots and fine-tuning AI/ML models in free time.
''')

    with col4:
        st.subheader('Sukhdeep')
        st.write('''Hello everyone! I'm Sukhdeep Singh. 
- Health Systems Performance Analyst at Inova Hospitals.
- Master's student in DAEN at GMU, specializing in data analytics.
- Experienced in working with pharmaceutical and patient data.
- Proficient in data analytics, statistics, and computer skills.
- Skilled in Python for healthcare data and Tableau for visualization.
''')


    with col5:
        st.subheader('Aqsa')
        st.write('''Hi, I'm Aqsa Janjuah. 
- Master's student in Data Analytics Engineering, specializing in Predictive Analytics and Applied Analytics.
- Data engineer at Deloitte with 2 years of experience.
- Experienced in data pipelines, ETL, and data visualization.
- Proficient in NLP, ML/AI, and Predictive Analytics.
''')


    with col6:
        st.subheader('Sid')
        st.write('''My name is Sidney G. Beck
- Army Warrant Officer with over 16 years of intelligence and security experience.
- Pursuing a master's degree in Data Analytics Engineering at George Mason University.
- Proficient in Big Data Analytics, Python, R programming, and machine learning.
- Skilled in Python and R, with a preference for Python's versatility.
''')

