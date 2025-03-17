import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Sample Property Data (Replace with real data if available)
data = [
    {"location": "Los Angeles", "bedrooms": 5, "bathrooms": 4, "area_sqft": 4500, "price": 2500000},
    {"location": "New York", "bedrooms": 2, "bathrooms": 2, "area_sqft": 1500, "price": 1200000},
    {"location": "Miami", "bedrooms": 4, "bathrooms": 3, "area_sqft": 3200, "price": 1800000},
    {"location": "Denver", "bedrooms": 3, "bathrooms": 2, "area_sqft": 1800, "price": 750000},
    {"location": "Chicago", "bedrooms": 3, "bathrooms": 3, "area_sqft": 2600, "price": 2200000},
    {"location": "Austin", "bedrooms": 4, "bathrooms": 3, "area_sqft": 3500, "price": 900000},
    {"location": "San Francisco", "bedrooms": 1, "bathrooms": 1, "area_sqft": 800, "price": 650000},
    {"location": "Seattle", "bedrooms": 3, "bathrooms": 2, "area_sqft": 2000, "price": 1100000},
    {"location": "Las Vegas", "bedrooms": 2, "bathrooms": 2, "area_sqft": 1600, "price": 1350000},
    {"location": "Boston", "bedrooms": 3, "bathrooms": 3, "area_sqft": 2300, "price": 1750000},
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert "location" to numerical values
df["location"] = df["location"].astype("category").cat.codes

# Features & Target
X = df[["location", "bedrooms", "bathrooms", "area_sqft"]]
y = df["price"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "price_model.pkl")

print("✅ Price Prediction Model Trained & Saved Successfully!")
