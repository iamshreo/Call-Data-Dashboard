import pandas as pd
import re

df = pd.read_csv("sample_call_logs.csv", dtype=str)

df_cleaned = df.drop_duplicates(subset=["Company Name", "Phone"], keep="first")

df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")

def normalize_phone(phone, country_code="+91"):
    if pd.isna(phone) or phone.strip() == "":
        return "Not Available"
    digits = re.sub(r"\D", "", phone)
    if digits.startswith(country_code.replace("+", "")):
        return f"+{digits}"
    return country_code + digits

df["Phone"] = df["Phone"].apply(normalize_phone)

df["Interested"] = df["Interested"].fillna("Not Replied")
df["Whatsapp"] = df["Whatsapp"].fillna("Not Replied")

df["Follow UP date"] = pd.to_datetime(df["Follow UP date"], errors="coerce", dayfirst=True)
df["Follow UP date"] = df["Follow UP date"].dt.strftime("%Y-%m-%d").fillna("Not Scheduled")

df["Follow UP"] = df["Follow UP"].replace("", "Follow-up pending").fillna("Follow-up pending")

df.rename(columns={"Phone": "Phone No"}, inplace=True)

df.to_csv("new_call_data.csv", index=False)



