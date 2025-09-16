import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(page_title="Call Data Dashboard", layout="wide")

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
        
        phone_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" 
            width="28" height="28" style="vertical-align: middle; margin-right: 10px;">
        <path d="M21 16.42V19.9561C21 20.4811 20.5941 20.9167 20.0705 20.9537C19.6331 20.9846 19.2763 21 19 21C10.1634 21 3 13.8366 3 5C3 4.72371 3.01545 4.36687 3.04635 3.9295C3.08337 3.40588 3.51894 3 4.04386 3H7.5801C7.83678 3 8.05176 3.19442 8.07753 3.4498C8.10067 3.67907 8.12218 3.86314 8.14207 4.00202C8.34435 5.41472 8.75753 6.75936 9.3487 8.00303C9.44359 8.20265 9.38171 8.44159 9.20185 8.57006L7.04355 10.1118C8.35752 13.1811 10.8189 15.6425 13.8882 16.9565L15.4271 14.8019C15.5572 14.6199 15.799 14.5573 16.001 14.6532C17.2446 15.2439 18.5891 15.6566 20.0016 15.8584C20.1396 15.8782 20.3225 15.8995 20.5502 15.9225C20.8056 15.9483 21 16.1633 21 16.42Z"></path>
        </svg>
        """
        st.markdown(
            f"<h1 style='display: flex; align-items: center;'>{phone_svg} Call Data Dashboard</h1>",
            unsafe_allow_html=True
        )

        total_companies = df["Company Name"].nunique()
        total_categories = df["Category"].nunique()
        followup_done = df["Follow UP"].str.contains("Completed", case=False, na=False).sum()
        followup_pending = df["Follow UP"].str.contains("pending", case=False, na=False).sum()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label=" Total Companies", value=total_companies)

        with col2:
            st.metric(label=" Categories", value=total_categories)

        with col3:
            st.metric(label=" Follow-up Done", value=followup_done)

        with col4:
            st.metric(label=" Follow-up Pending", value=followup_pending)

        st.markdown("---")

        # interested graph ---------------------------------------------------------------

        total_leads = len(df)
        interested_leads = df[df['Interested'].str.upper() == "YES"].shape[0]
        interested_percent = round((interested_leads / total_leads) * 100, 2) if total_leads > 0 else 0

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=interested_percent,
            delta={'reference': 50},  
            title={'text': "Interested Leads %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#ed1b2e"},  
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': interested_percent
                }
            }
        ))

        st.plotly_chart(fig, use_container_width=True)


        # notification---------------------------

        pending_followups = df[df["Follow UP"].str.contains("pending", case=False, na=False)]
        if not pending_followups.empty:
            st.toast(f"⚠️ You have {len(pending_followups)} pending follow-ups!", icon="⚠️")

        st.markdown("---")

        valid_followups = df.dropna(subset=["Follow UP date"])
        sorted_followups = valid_followups.sort_values("Follow UP date")
        next_five = sorted_followups.head(5)

        st.subheader("🔔 Upcoming Follow-ups")
        if next_five.empty:
            st.success("✅ No upcoming follow-ups.")
        else:
            st.table(
                next_five[["Company Name", "Follow UP date", "Category", "Call Details"]]
                .rename(columns={
                    "Company Name": "Company",
                    "Follow UP date": "Follow-up Date",
                    "Category": "Category",
                    "Call Details": "Call Status"
                })
            )

        st.markdown("---")
        
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
        elif whatsapp_filter =="YES":
            st.write("Companies with WhatsApp (YES):", whatsapp_counts.get("YES", 0))
        elif whatsapp_filter =="NO":
            st.write("Companies with WhatsApp (NO):", whatsapp_counts.get("NO", 0))
        

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
            companies_per_category = unique_companies["Category"].value_counts().reset_index()
            companies_per_category.columns = ["Category", "Count"]

            fig2 = px.pie(
                companies_per_category,
                values="Count",
                names="Category",
                title="Companies per Category",
                hole=0.3, 
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                legend_title="Category",
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.05
                )
            )

            st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------------------------------------------------------------------------------------------------
                    
        with right:
            st.subheader("Call Outcomes Distribution")

            outcomes_df = pd.DataFrame({
                "Call Outcome": list(outcome_counts.keys()),
                "Number of Calls": list(outcome_counts.values())
            })

            fig = px.bar(
                outcomes_df,
                x="Call Outcome",
                y="Number of Calls",
                color="Call Outcome",   
                text="Number of Calls", 
                title="Call Outcomes Distribution",
                color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"] 
            )

            fig.update_traces(textposition="outside")  
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",   
                paper_bgcolor="rgba(0,0,0,0)",  
                xaxis_title="Call Outcome",
                yaxis_title="Number of Calls",
                legend_title="Call Outcome",
                legend=dict(
                    orientation="h",   
                    yanchor="bottom",
                    y=1.05,
                    xanchor="right",
                    x=1
                )
            )

            st.plotly_chart(fig, use_container_width=True)

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
    
    filter_svg ="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"width="28" height="28" style="vertical-align: middle; margin-right: 10px;"><path d="M21 4V6H20L15 13.5V22H9V13.5L4 6H3V4H21ZM6.4037 6L11 12.8944V20H13V12.8944L17.5963 6H6.4037Z"></path></svg>"""   

                             
    st.markdown(
            f"<h1 style='display: flex; align-items: center;'>{filter_svg} Data Filter Dashboard</h1>",
            unsafe_allow_html=True
        )

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        col_category = "Category"
        category_options = ["All"] + sorted(df[col_category].dropna().unique().tolist())
        selected_category = st.selectbox("Category", category_options, help="Filter companies by category (e.g., Interior Designer , Real Estate).")

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

    excel_svg="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"width="28" height="28" style="vertical-align: middle; margin-right: 10px;"><path d="M2.85858 2.87732L15.4293 1.0815C15.7027 1.04245 15.9559 1.2324 15.995 1.50577C15.9983 1.52919 16 1.55282 16 1.57648V22.4235C16 22.6996 15.7761 22.9235 15.5 22.9235C15.4763 22.9235 15.4527 22.9218 15.4293 22.9184L2.85858 21.1226C2.36593 21.0522 2 20.6303 2 20.1327V3.86727C2 3.36962 2.36593 2.9477 2.85858 2.87732ZM4 4.73457V19.2654L14 20.694V3.30599L4 4.73457ZM17 19H20V4.99997H17V2.99997H21C21.5523 2.99997 22 3.44769 22 3.99997V20C22 20.5523 21.5523 21 21 21H17V19ZM10.2 12L13 16H10.6L9 13.7143L7.39999 16H5L7.8 12L5 7.99997H7.39999L9 10.2857L10.6 7.99997H13L10.2 12Z"></path></svg>"""

    if st.session_state.page == "View Excel File":
        st.subheader("View and Edit Excel Data")

        edited_df = st.data_editor(df, num_rows="dynamic") 

        if st.button("Save Changes"):
            edited_df.to_csv("new_call_data.csv", index=False)
            st.success("✅ Changes saved successfully!")
            df = edited_df.copy()


# ----------------------------------------------------------------------------------------------------------------------------------------------------

elif st.session_state.page == "Search":

    search_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"width="28" height="28" style="vertical-align: middle; margin-right: 10px;"><path d="M18.031 16.6168L22.3137 20.8995L20.8995 22.3137L16.6168 18.031C15.0769 19.263 13.124 20 11 20C6.032 20 2 15.968 2 11C2 6.032 6.032 2 11 2C15.968 2 20 6.032 20 11C20 13.124 19.263 15.0769 18.031 16.6168ZM16.0247 15.8748C17.2475 14.6146 18 12.8956 18 11C18 7.1325 14.8675 4 11 4C7.1325 4 4 7.1325 4 11C4 14.8675 7.1325 18 11 18C12.8956 18 14.6146 17.2475 15.8748 16.0247L16.0247 15.8748Z"></path></svg>"""

    st.markdown(f"<h1 style='display: flex; align-items: center;'>{search_svg} Search Data </h1> ",
                unsafe_allow_html=True
                )
    search_term = st.text_input("Enter search term for Company Name:")
    
    results = pd.DataFrame()
    if search_term:
        results = df[df["Company Name"].str.contains(search_term, case=False, na=False)]
        st.write(f"Found {len(results)} results:")
    st.dataframe(results)

# ----------------------------------------------------------------------------------------------------------------------------------------------------

elif st.session_state.page == "Add Data":

    add_data_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"width="28" height="28" style="vertical-align: middle; margin-right: 10px;"><path d="M14 14.252V16.3414C13.3744 16.1203 12.7013 16 12 16C8.68629 16 6 18.6863 6 22H4C4 17.5817 7.58172 14 12 14C12.6906 14 13.3608 14.0875 14 14.252ZM12 13C8.685 13 6 10.315 6 7C6 3.685 8.685 1 12 1C15.315 1 18 3.685 18 7C18 10.315 15.315 13 12 13ZM12 11C14.21 11 16 9.21 16 7C16 4.79 14.21 3 12 3C9.79 3 8 4.79 8 7C8 9.21 9.79 11 12 11ZM18 17V14H20V17H23V19H20V22H18V19H15V17H18Z"></path></svg>"""
    st.markdown(f"<h1 style='display: flex; align-items: center;'>{add_data_svg} Add Bulk Data </h1> ",
                unsafe_allow_html=True
                )
    
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                new_df = pd.read_csv(uploaded_file, dtype=str)
            else:
                new_df = pd.read_excel(uploaded_file, dtype=str)

            st.write("Preview of uploaded file:")
            st.dataframe(new_df.head())

            if "Company Name" in new_df.columns and "Phone" in new_df.columns:
                new_df = new_df.drop_duplicates(subset=["Company Name", "Phone"], keep="first")

            if "DATE" in new_df.columns:
                new_df["DATE"] = pd.to_datetime(new_df["DATE"], errors="coerce", dayfirst=True)
                new_df["DATE"] = new_df["DATE"].dt.strftime("%Y-%m-%d")

            def normalize_phone(phone, country_code="+91"):
                if pd.isna(phone) or str(phone).strip() == "":
                    return "Not Available"
                digits = re.sub(r"\D", "", str(phone))
                if digits.startswith(country_code.replace("+", "")):
                    return f"+{digits}"
                return country_code + digits

            if "Phone" in new_df.columns:
                new_df["Phone"] = new_df["Phone"].apply(normalize_phone)
                new_df.rename(columns={"Phone": "Phone No"}, inplace=True)

            if "Interested" in new_df.columns:
                new_df["Interested"] = new_df["Interested"].fillna("Not Replied")
            if "Whatsapp" in new_df.columns:
                new_df["Whatsapp"] = new_df["Whatsapp"].fillna("Not Replied")

            if "Follow UP date" in new_df.columns:
                new_df["Follow UP date"] = pd.to_datetime(new_df["Follow UP date"], errors="coerce", dayfirst=True)
                new_df["Follow UP date"] = new_df["Follow UP date"].dt.strftime("%Y-%m-%d").fillna("Not Scheduled")

            if "Follow UP" in new_df.columns:
                new_df["Follow UP"] = new_df["Follow UP"].replace("", "Follow-up pending").fillna("Follow-up pending")

            new_df.to_csv("new_call_data.csv", mode="a", header=False, index=False)

            st.success("Bulk data cleaned and added successfully")
            st.dataframe(new_df.head())

        except Exception as e:
            st.error(f"Error processing file: {e}")
