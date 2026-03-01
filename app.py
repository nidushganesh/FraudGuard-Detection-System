import streamlit as st
import pandas as pd
import sqlite3

# 1. Setup and Sidebar Controls
st.set_page_config(page_title="FraudGuard Analyst Portal", layout="wide")
st.title("🛡️ FraudGuard: Analyst Dashboard")

threshold = st.sidebar.slider('Risk Threshold', 0.0, 1.0, 0.75)

# 2. Performance Metrics (Hardcoded from your Model Evaluation)
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Model Precision", "91%", "+29% vs Rules")
col_m2.metric("Model Recall", "92%", "+17% vs Rules")
col_m3.metric("Pending Alerts", "12") # Example count

# 3. Load and Filter Data
# (Assuming 'df' is loaded from your CSV/SQLite database)
# df = pd.read_sql('SELECT * FROM Transactions', conn) 
# For demonstration, we'll use your identified alerts A1023 and A1024
data = {
    'Alert ID': ['A1023', 'A1024'],
    'Transaction ID': ['International', 'High Frequency'],
    'Risk Score': [0.92, 0.87],
    'Status': ['Pending', 'Pending']
}
df = pd.DataFrame(data)
filtered_data = df[df['Risk Score'] >= threshold]

# 4. Interactive Transaction List
st.subheader("Transactions Awaiting Review")

if not filtered_data.empty:
    for index, row in filtered_data.iterrows():
        # Create a container for each alert
        with st.container():
            c1, c2, c3 = st.columns([4, 1, 1])
            
            with c1:
                st.write(f"**Alert:** {row['Alert ID']} | **Score:** {row['Risk Score']} | **Type:** {row['Transaction ID']}")
            
            with c2:
                # Use unique keys to avoid Streamlit DuplicateWidgetID error
                if st.button("Approve", key=f"app_{row['Alert ID']}"):
                    st.success(f"Transaction {row['Alert ID']} Approved.")
                    # Add SQL UPDATE logic here: 
                    # conn.execute("UPDATE Transactions SET Status='APPROVED' WHERE ID=?", (row['Alert ID'],))
            
            with c3:
                if st.button("Block", key=f"blk_{row['Alert ID']}"):
                    st.error(f"Transaction {row['Alert ID']} Blocked.")
                    # Add SQL UPDATE logic here
            
            st.divider()
else:
    st.info("No transactions meet the current risk threshold.")