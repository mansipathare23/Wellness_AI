# goal_tracker.py

import streamlit as st
import pandas as pd
import os
from datetime import datetime

def goal_tracker_page():
    st.title("🎯 Goal Tracker")
    
    # Check if goals.csv exists; if not, create it
    if not os.path.exists("goals.csv"):
        df = pd.DataFrame(columns=["date", "goal", "status"])
        df.to_csv("goals.csv", index=False)

    # Load existing goals
    df = pd.read_csv("goals.csv")

    # Form to add a new goal
    st.subheader("➕ Add a New Goal")
    new_goal = st.text_input("Your Goal")
    if st.button("Add Goal"):
        if new_goal:
            new_entry = {"date": datetime.now().date(), "goal": new_goal, "status": "Pending"}
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv("goals.csv", index=False)
            st.success("Goal added!")
            st.experimental_rerun()

    # Display current goals
    st.subheader("📋 Your Goals")
    if df.empty:
        st.info("No goals added yet.")
    else:
        edited_df = st.data_editor(df, use_container_width=True, key="goals_editor")
        df.update(edited_df)
        df.to_csv("goals.csv", index=False)
