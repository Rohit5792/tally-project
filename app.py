import pandas as pd
import streamlit as st

# ---- Load file ----
file_path = "Transactions.txt"
df = pd.read_csv(file_path, header=None, encoding="utf-16")
new_df = pd.DataFrame(df)

# Assign column names
new_df.columns = ["Date", "Client", "Col3", "Type", "Debit", "Credit", "Extra"]
new_df = new_df[["Date", "Client", "Type", "Debit", "Credit"]]

# Convert Debit/Credit to numeric
new_df["Debit"] = pd.to_numeric(new_df["Debit"], errors="coerce").fillna(0)
new_df["Credit"] = pd.to_numeric(new_df["Credit"], errors="coerce").fillna(0)

# ---- Function to get client records and balance ----
def get_client_records(client_name):
    records = new_df[new_df["Client"].str.contains(client_name, case=False, na=False, regex=False)]
    total_debit = records["Debit"].sum() * -1
    total_credit = records["Credit"].sum()
    balance = total_debit - total_credit
    return records, total_debit, total_credit, balance

# ---- Streamlit UI ----
st.set_page_config(page_title="Client Transactions Search", layout="wide")
st.title("🔍 Client Transactions Search")

search_keyword = st.text_input("Enter client name keyword:")

if search_keyword:
    # Split user input into individual words
    keywords = search_keyword.split()

    # Build regex to match ANY of the words
    pattern = "|".join(keywords)

    # Find matches in Client column
    matching_clients = new_df[new_df["Client"].str.contains(pattern, case=False, na=False)]["Client"].unique()

    if len(matching_clients) == 0:
        st.error("❌ No clients found with that keyword.")
    else:
        st.subheader("✅ Matching Clients")
        
        # Step 3: Let user click one client (radio button)
        selected_client = st.radio("Select a client:", matching_clients)

        # Step 4: Show transactions
        if selected_client:
            records, total_debit, total_credit, balance = get_client_records(selected_client)

            st.subheader(f"📄 Transactions for: {selected_client}")

            if records.empty:
                st.warning("No records found")
            else:
                # Show table
                st.dataframe(records, use_container_width=True)

                # Show totals
                st.markdown(f"**Total Quoatation:** {total_debit}")
                st.markdown(f"**Total Credit (Received):** {total_credit}")
                st.markdown(
                    f"<span style='color:red; font-weight:bold'>Balance: {balance}</span>",
                    unsafe_allow_html=True
                )


