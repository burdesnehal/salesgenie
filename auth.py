import bcrypt, db

def hash_pwd(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def check_pwd(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_user(username, email, password):
    # uniqueness check
    dup = db.run(
        "SELECT id FROM users WHERE username=%s OR email=%s",
        (username, email),
        fetchone=True
    )
    if dup:
        return False, "Username or email already exists."

    db.run(
        "INSERT INTO users (username, email, pwd_hash) VALUES (%s, %s, %s)",
        (username, email, hash_pwd(password))
    )
    return True, "Account created. Please log in."

def authenticate(usr_or_email, password):
    user = db.run(
        "SELECT * FROM users WHERE username=%s OR email=%s",
        (usr_or_email, usr_or_email),
        fetchone=True
    )
    if user and check_pwd(password, user["pwd_hash"]):
        return user
    return None
