import bcrypt


def create_user_table(conn):
    """
    Create the 'users' table if it doesn't exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()


def register_user(conn, username, password, firstname, lastname):
    """
    Register a new user by inserting their username and hashed password into the 'users' table.
    """
    cursor = conn.cursor()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert the user into the 'users' table
    cursor.execute("""
        INSERT INTO users (username, password, firstname, lastname, role)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, hashed_password, firstname, lastname, "normal"))

    conn.commit()
    cursor.close()


def authenticate_user(conn, username, password):
    """
    Authenticate a user by checking their username and password against the 'users' table.
    Returns True if the user is authenticated, False otherwise.
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
        SELECT password FROM users WHERE username = %s
    """, (username,))
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return False

    hashed_password = result[0].encode('utf-8')

    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def get_first_and_last_names_and_role(conn, username):
    """
    Get first and last name of user
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
            SELECT firstname, lastname, role FROM users WHERE username = %s
        """, (username,))
    result = cursor.fetchone()
    cursor.close()

    return [result[0], result[1], result[2]]


def get_user_all_info(conn, username):
    """
    Get all info of user
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
            SELECT username, firstname, lastname, role FROM users WHERE username = %s
        """, (username,))
    result = cursor.fetchone()
    cursor.close()

    return result

def get_all_users(conn):
    """
    Get all info of users table
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
            SELECT username, firstname, lastname, role FROM users
        """)
    result = cursor.fetchall()
    cursor.close()

    return result


def promote_user(conn, username):
    """
    Promote user to admin
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
            UPDATE users
            SET role = 'admin'
            WHERE username = %s
        """, (username,))
    conn.commit()
    cursor.close()


def demote_user(conn, username):
    """
    Demote user to normal
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
            UPDATE users
            SET role = 'normal'
            WHERE username = %s
        """, (username,))
    conn.commit()
    cursor.close()


def delete_user(conn, username):
    """
    Delete user
    """
    cursor = conn.cursor()

    # Retrieve the hashed password from the 'users' table
    cursor.execute("""
            DELETE FROM users WHERE username = %s
        """, (username,))
    conn.commit()
    cursor.close()
