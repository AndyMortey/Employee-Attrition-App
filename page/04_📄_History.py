import streamlit as st
import pandas as pd
import os
import streamlit_authenticator as stauth

# Function to load history data
@st.cache_data(persist=True)
def load_history():
    csv_path = "Data/history.csv"  # Adjust the path accordingly
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if file doesn't exist

def display_history_of_all_predictions():
    st.title("Prediction History📄")

    # Button to clear cache
    if st.button("Clear Cache"):
        st.cache_data.clear()

    # Load history data
    history = load_history()

    # Check if the history DataFrame is not empty
    if not history.empty:
        st.write("Here are the past predictions:")
        st.dataframe(history)
        
        # Download option for the history data
        st.subheader("Download Data")
        st.download_button(
            label="Download history as CSV",
            data=history.to_csv(index=False).encode('utf-8'),
            file_name='prediction_history.csv',
            mime='text/csv'
        )
    else:
        st.write("No history of predictions yet.")

# Run the Streamlit application
if __name__ == "__main__":
    display_history_of_all_predictions()
