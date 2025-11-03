# ML-Model-For-Customer-Conversion-Insights
End-to-end ML pipeline for understanding what drives customer conversion. Predict customer conversion from product features and review sentiment using Snowflake ML and Cortex. Includes explainability, NLP diagnostics, and a Streamlit dashboard for business insight.

Disclamer: This project was forked from Snowflake-Labs, and modified:
[https://github.com/Snowflake-Labs/sfguide-build-ml-models-for-customer-conversions.git ](https://github.com/Snowflake-Labs/sfguide-build-ml-models-for-customer-conversions.git)



PROJECT STRUCTURE
├── README.md
├── Customer Conversions.ipynb      # Full Snowflake ML pipeline (rebuilt from Snowflake's lab)
├── streamlit_CCapp.py              # The interactive dashboard (coded with Copilot)
├── EnableCrossRegion.sql           # Configuration for cross-region Snowflake access
├── Setup ACCOUNTADMIN Role.sql     # Role setup
├── SetupGuide.txt                  # Step-by-step process
├── .gitignore                      # Ignore checkpoints, cache, etc.
├── assets/                         # Optional: screenshots or visuals
   └── Dashboard_ML.jpg
   └── Dashboard_NLP.jpg
   └── Environment Setup.jpg
└── data/                           # Synthetic data
   └── synthetic_review_data_sourcetable.csv
   └── synthetic_review_data_text.txt

# 🧠 Customer Conversion Lab

This lab demonstrates how to build an end-to-end machine learning (ML) pipeline in Snowflake to predict customer conversion based on product features, review sentiment, and NLP signals — and visualize the results in an interactive Streamlit dashboard.

---

🚀 Features

- Train and deploy an XGBoost model using Snowflake ML
- Enrich reviews with sentiment using Snowflake Cortex
- Segment users by conversion likelihood and emotional tone
- Diagnose model residuals and feature impact
- Explore insights in a Streamlit dashboard

---

📊 Interactive Dashboard 

https://app.snowflake.com/.../#/streamlit-apps/HOL_DB.HOL_SCHEMA.NZC_RN57VD3SQK25

NOTE: Streamlit share features are not currently supported when using Streamlit in a Snowflake Native App: Custom components are not supported.Using Azure Private Link and Google Cloud Private Service Connect to access a Streamlit app is not supported.
---
