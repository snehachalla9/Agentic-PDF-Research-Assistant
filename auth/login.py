import streamlit as st
from auth.auth import login


def login_page():
    st.title("🔐 Login")

    st.write("Welcome back! Login to continue.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # Validation
        if not email or not password:
            st.warning("Please enter both email and password.")

        else:
            result = login(email, password)

            # Login Successful
            if hasattr(result, "user") and result.user:

                st.session_state["logged_in"] = True
                st.session_state["user"] = result.user

                st.success("✅ Login Successful!")

                st.rerun()

            else:
                st.error("Invalid email or password.")


if __name__ == "__main__":
    login_page()