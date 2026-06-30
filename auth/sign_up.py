import streamlit as st
from auth.auth import sign_up


def signup_page():
    st.title("📝 Create an Account")

    st.write("Sign up to start using the AI PDF Assistant.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):

        # Validation
        if not email or not password or not confirm_password:
            st.warning("Please fill all the fields.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")

        else:
            result = sign_up(email, password)

            # Check for successful signup
            if hasattr(result, "user") and result.user:
                st.success("✅ Account created successfully!")

                st.info(
                    "If email confirmation is enabled in Supabase, "
                    "please verify your email before logging in."
                )

            else:
                st.error(str(result))


if __name__ == "__main__":
    signup_page()