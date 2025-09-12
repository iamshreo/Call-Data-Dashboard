import pandas as pd

import matplotlib.pyplot as plt


df = pd.read_csv("new_call_data.csv", dtype=str)


print("The number of companies are :- ", df["Company Name"].nunique())

picked_up = df["Call Details"].str.contains("Called", case=False, na=False).sum()
print("Picked Up Calls :- ", picked_up)

not_picked_up = df["Call Details"].str.contains("Did not pick up", case=False, na=False).sum()
print("Did Not Pick Up calls :- ", not_picked_up)

invalid_numbers = df["Call Details"].str.contains("Invalid", case=False, na=False).sum()
print("Invalid Numbers :- ", invalid_numbers)

need_follo_update = df["Follow UP date"].str.contains("Not Scheduled", case=False, na=False).sum()
print("Follow UP date :- ", need_follo_update)



outcome_counts = {
    "Called": picked_up,
    "Did not pick up": not_picked_up,
    "Invalid": invalid_numbers
}



def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        count = int(round(pct*total/100.0))
        return f"{count} ({pct:.1f}%)"
    return my_format

plt.figure(figsize=(6,6))
plt.pie(outcome_counts.values(),labels=outcome_counts.keys(),autopct=autopct_format(list(outcome_counts.values())),startangle=90)
plt.title("Call Outcomes Distribution")
plt.show()



df["Number of calls"] = pd.to_numeric(df["Number of calls"], errors="coerce").fillna(0)

calls_per_company = df.groupby("Company Name")["Number of calls"].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
calls_per_company.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Number of Calls per Company")
plt.xlabel("Company Name")
plt.ylabel("Number of Calls")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
