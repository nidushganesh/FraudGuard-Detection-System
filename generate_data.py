import pandas as pd
import numpy as np

# Creating a synthetic dataset of 1000 transactions
data = {
    'Amount': np.random.uniform(10, 5000, 1000),
    'Merchant_Category': np.random.choice(['Retail', 'Online', 'ATM', 'Transfer'], 1000),
    'Currency_Type': np.random.choice(['LKR', 'GBP'], 1000),
    'Hour_of_Day': np.random.randint(0, 24, 1000),
    'Is_Fraud': np.random.choice([0, 1], 1000, p=[0.95, 0.05]) # 5% Fraud rate
}

df = pd.DataFrame(data)
df.to_csv('transaction_data.csv', index=False)
print("transaction_data.csv has been created successfully!")