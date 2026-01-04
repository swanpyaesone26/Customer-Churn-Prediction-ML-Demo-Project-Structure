import streamlit as st
import pandas as pd
import joblib
from customer_churn_prediction.src.preprocessing import build_encoder

# Load model
model = joblib.load("customer_churn_prediction/data/05-final-churn-model.joblib")

# Build an encoder matching the training one-hot scheme
encoder = build_encoder()

feature_names = joblib.load("customer_churn_prediction/data/06-feature-names.joblib")

st.title("Customer Churn Prediction")
st.write("Enter customer details to check the risk of leaving the bank.")

col1, col2 = st.columns(2)

with col1:
    credit_score = st.number_input(
        "Credit Score", min_value=300, max_value=850, value=600
    )
    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=100, value=30)

with col2:
    tenure = st.slider("Tenure (Years)", 0, 20, 5)
    balance = st.number_input("Balance", min_value=0.0, value=10000.0)
    num_products = st.slider("Number of Products", 1, 6, 1)
    has_crcard = st.selectbox("Has Credit Card?", ["Yes", "No"])
    is_active = st.selectbox("Is Active Member?", ["Yes", "No"])
    estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0)


if st.button("Predict Risk"):
    input_data = pd.DataFrame(
        [
            {
                "CreditScore": credit_score,
                "Geography": geography,
                "Gender": gender,
                "Age": age,
                "Tenure": tenure,
                "Balance": balance,
                "NumOfProducts": num_products,
                "HasCrCard": has_crcard,
                "IsActiveMember": is_active,
                "EstimatedSalary": estimated_salary,
            }
        ]
    )

    # Convert Yes/No fields to numeric (0/1) to match training dtypes
    input_data["HasCrCard"] = (
        input_data["HasCrCard"].map({"Yes": 1, "No": 0}).astype(int)
    )
    input_data["IsActiveMember"] = (
        input_data["IsActiveMember"].map({"Yes": 1, "No": 0}).astype(int)
    )

    encoded_features = encoder.transform(input_data[["Geography", "Gender"]])
    new_cols = encoder.get_feature_names_out(["Geography", "Gender"])
    encoded_df = pd.DataFrame(
        encoded_features, columns=new_cols, index=input_data.index
    )

    final_input = pd.concat(
        [input_data.drop(["Geography", "Gender"], axis=1), encoded_df], axis=1
    )

    final_input = final_input[feature_names]

    prob = model.predict_proba(final_input)[0, 1]

    threshold = 0.35
    prediction = 1 if prob >= threshold else 0

    st.subheader(f"Churn Probability: {prob:.2%}")

    if prediction == 1:
        st.error("HIGH RISK: This customer is likely to leave.")
    else:
        st.success("LOW RISK: This customer is likely to stay.")
