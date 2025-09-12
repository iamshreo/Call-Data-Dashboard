import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="Call Data Dashboard", layout="wide")


st.title("Call Data Dashboard")


df = pd.read_csv("new_call_data.csv", dtype=str)

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("Navigation")
if st.sidebar.button(" Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Filter Data"):
    st.session_state.page = "Filter Data"
if st.sidebar.button("View Excel File"):
    st.session_state.page = "View Excel File"
if st.sidebar.button("Search"):
    st.session_state.page = "Search"
if st.sidebar.button("Add Data"):
    st.session_state.page = "Add Data"

# -------------------------------------------------------------------------------------------------------------------------------------------------

if st.session_state.page == "Home":
        
        st.subheader("Summary Metrics")
        st.write("Total number of companies:", df["Company Name"].nunique())

        st.markdown("---")

        selected_date = st.selectbox("Select a date", df["DATE"].unique())

            
        filtered_df = df[df["DATE"] == selected_date]

        
        picked_up = filtered_df["Call Details"].str.contains("Called", case=False, na=False).sum()
        not_picked_up = filtered_df["Call Details"].str.contains("Did not pick up", case=False, na=False).sum()
        invalid_numbers = filtered_df["Call Details"].str.contains("Invalid", case=False, na=False).sum()

            
        st.subheader(f"Calls on date :- {selected_date}")
        st.write("Picked Up Calls:- ", picked_up)
        st.write("Did Not Pick Up Calls:- ", not_picked_up)
        st.write("Invalid Numbers:- ", invalid_numbers)

        st.markdown("---")



        st.subheader("Filter Companies by WhatsApp Availability")


        whatsapp_counts = df["Whatsapp"].value_counts()

        whatsapp_filter = st.selectbox("Show companies with WhatsApp:", ["All", "Yes", "No"])

        if whatsapp_filter == "All":
            st.write("Companies with WhatsApp (YES):", whatsapp_counts.get("YES", 0))
            st.write("Companies without WhatsApp (NO):", whatsapp_counts.get("NO", 0))
        

        # ------------------------------------------------------------------------------------------------------------------------

        st.markdown("---")

        st.subheader(f"All Call Count :- ")
        picked_up = df["Call Details"].str.contains("Called", case=False, na=False).sum()
        not_picked_up = df["Call Details"].str.contains("Did not pick up", case=False, na=False).sum()
        invalid_numbers = df["Call Details"].str.contains("Invalid", case=False, na=False).sum()
        need_follow_up = df["Follow UP date"].str.contains("Not Scheduled", case=False, na=False).sum()

        st.write("Picked Up Calls:- ", picked_up)
        st.write("Did Not Pick Up Calls:- ", not_picked_up)
        st.write("Invalid Numbers:- ", invalid_numbers)
        st.write("Follow UP Not Scheduled:-", need_follow_up)

        outcome_counts = {
            "Called": picked_up,
            "Did not pick up": not_picked_up,
            "Invalid": invalid_numbers
        }

# ---------------------------------------------------------------------------------------------------------------------------------------
        
        left,right=st.columns([1,1])

        with left:
            st.subheader("Number of Companies per Category")

            unique_companies = df.drop_duplicates(subset=["Company Name", "Category"])
            companies_per_category = unique_companies["Category"].value_counts()

            fig2, ax2 = plt.subplots(figsize=(4.5, 4.7))
            companies_per_category.plot(kind="bar", color="lightgreen", edgecolor="black", ax=ax2)
            ax2.set_xlabel("Category", fontsize=8)
            ax2.set_ylabel("Number of Companies", fontsize=8)
            ax2.set_title("Companies per Category")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig2)

# --------------------------------------------------------------------------------------------------------------------------------------------
                    
        with right :
            def autopct_format(values):
                def my_format(pct):
                    total = sum(values)
                    count = int(round(pct*total/100.0))
                    return f"{count} ({pct:.1f}%)"
                return my_format
            st.subheader("Call Outcomes Distribution")
            fig1, ax1 = plt.subplots(figsize=(4,4))
            ax1.pie(outcome_counts.values(),
                    labels=outcome_counts.keys(),
                    autopct=autopct_format(list(outcome_counts.values())),
                    startangle=90)
            ax1.set_title("Call Outcomes")
            st.pyplot(fig1)

 # -----------------------------------------------------------------------------------------------------------------------------------------

        df["DATE"] = pd.to_datetime(df["DATE"],errors="coerce")

        df["Year"] = df["DATE"].dt.year
        df["Month"] = df["DATE"].dt.month_name()

        st.subheader("Filter Raw Data by Month and Year")

        selected_year = st.selectbox("Select Year", sorted(df["Year"].dropna().unique()))


        sorted(df["Year"].dropna().unique())

        selected_month = st.selectbox("Select Month", sorted(df["Month"].dropna().unique()))


        filtered_raw = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)]

        st.write(f"### Raw Data for {selected_month},{selected_year}")
        st.dataframe(filtered_raw)

# ---------------------------------------------------------------------------------------------------------------------------------------------------
    

elif st.session_state.page == "Filter Data":
    

    st.title("Call Data Filter Dashboard")

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        col_category = "Category"
        category_options = ["All"] + sorted(df[col_category].dropna().unique().tolist())
        selected_category = st.selectbox("Category", category_options, help="Filter companies by category (e.g., Retail, IT, Services).")

    with col2:
        available_dates = sorted(df["DATE"].dropna().dt.date.unique())
        selected_date = st.selectbox("Select Dates",available_dates,
            help=" Pick a specific date to view call details.")

    with col3:
        col_call = "Call Details"
        call_options = ["All"] + sorted(df[col_call].dropna().unique().tolist())
        selected_call = st.selectbox("Call Details", call_options,
            help="Filter calls by status (Picked up, Did not pick up, Invalid).")

    with col4:
        col_followup = [c for c in df.columns if "Follow" in c][0]  
        followup_options = ["All"] + sorted(df[col_followup].dropna().unique().tolist())
        selected_followup = st.selectbox("Follow Up", followup_options,
            help="Show leads based on their follow-up status.")

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df[col_category] == selected_category]

    if selected_date:
        filtered_df = filtered_df[filtered_df["DATE"].dt.date == selected_date]

    if selected_call != "All":
        filtered_df = filtered_df[filtered_df[col_call] == selected_call]

    if selected_followup != "All":
        filtered_df = filtered_df[filtered_df[col_followup] == selected_followup]

    st.subheader("Filtered Data")
    st.write(f"Total rows: {len(filtered_df)}")
    st.dataframe(filtered_df)

# ----------------------------------------------------------------------------------------------------------------------------------------------------

elif st.session_state.page == "View Excel File":
    st.title("View Excel File")
    st.write("Showing raw CSV data:")
    st.dataframe(df)

# ----------------------------------------------------------------------------------------------------------------------------------------------------

elif st.session_state.page == "Search":
    st.title("Search Data")
    search_term = st.text_input("Enter search term for Company Name:")
    results = pd.DataFrame()
    if search_term:
        results = df[df["Company Name"].str.contains(search_term, case=False, na=False)]
        st.write(f"Found {len(results)} results:")
    st.dataframe(results)

# ----------------------------------------------------------------------------------------------------------------------------------------------------

elif st.session_state.page == "Add Data":
    
    st.title("Add Bulk Data")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv", "xlsx"])





