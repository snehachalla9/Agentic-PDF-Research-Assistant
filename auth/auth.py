from database.supabase import supabase


# -----------------------------
# Sign Up
# -----------------------------
def sign_up(email: str, password: str):
    """
    Register a new user using Supabase Authentication.
    """
    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )
        return response

    except Exception as e:
        return str(e)


# -----------------------------
# Login
# -----------------------------
def login(email: str, password: str):
    """
    Login an existing user.
    """
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )
        return response

    except Exception as e:
        return str(e)


# -----------------------------
# Logout
# -----------------------------
def logout():
    """
    Logout the currently logged in user.
    """
    try:
        supabase.auth.sign_out()
        return True

    except Exception as e:
        return str(e)


# -----------------------------
# Get Current User
# -----------------------------
def get_current_user():
    """
    Returns the currently logged in user.
    """
    try:
        response = supabase.auth.get_user()
        return response.user

    except Exception:
        return None