import streamlit_authenticator as stauth

# Correct way: use 'passwords' as a keyword argument
hashed_passwords = stauth.Hasher(passwords=['abc', 'def']).generate()

# Output the hashed passwords
for pwd in hashed_passwords:
    print(pwd)