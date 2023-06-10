import datetime

def create_players_table(conn):
    """
    Create the 'db' table if it doesn't exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            timeslot TIMESTAMP NOT NULL,
            dateRegistration TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    cursor.close()


def register_player(conn, username, timeslot):
    """
    Register a player by inserting their username and timestamp they want to play into the 'db' table.
    """
    cursor = conn.cursor()

    # Insert the player into the 'db' table
    cursor.execute("""
        INSERT INTO players (username, timeslot, dateRegistration)
        VALUES (%s, %s, %s)
    """, (username, timeslot, datetime.datetime.now().replace(microsecond=0)))

    conn.commit()
    cursor.close()


def get_player_registrations(conn, username):
    """
    Get all registrations for the player
    """
    cursor = conn.cursor()

    # Insert the player into the 'db' table
    cursor.execute("""
        SELECT timeslot FROM players WHERE username = %s
    """, (username,))

    result = cursor.fetchall()
    cursor.close()

    return result


def get_all_players_registrations(conn):
    """
    Get all registrations for the player
    """
    cursor = conn.cursor()

    # Insert the player into the 'db' table
    cursor.execute("""
        SELECT username, timeslot, dateRegistration FROM players WHERE timeslot >= CURRENT_DATE ORDER BY dateRegistration ASC
    """)

    result = cursor.fetchall()
    cursor.close()

    return result

def cancel_player_registrations(conn, username, timeslot_to_delete):
    """
    Cancel registration for the player
    """
    cursor = conn.cursor()

    # Insert the player into the 'db' table
    cursor.execute("""
        DELETE FROM players WHERE username = %s AND timeslot = %s
    """, (username, timeslot_to_delete))

    conn.commit()
    cursor.close()

