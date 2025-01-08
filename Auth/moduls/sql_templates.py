class SQLTemplates:
    logger = {
        "database": {
            "insert_database_error": "INSERT INTO"
        },
        "user": {
            "insert_user_action": "INSERT INTO"
        }
    }

    user = {
        # Abfrage zur Überprüfung der Anmeldedaten
        "login": "SELECT count(`Username`) FROM `user_account` WHERE `Username` = %s AND `Password` = %s",

        # Abfrage zur Überprüfung eines Tokens (Access-Token)
        "check_access_token": "SELECT count(*) as count FROM `user_account` WHERE `UserID` = %s AND `access_token` = %s",

        # Abfrage zum Aktualisieren des Access-Tokens
        "update_access_token": "UPDATE `user_account` SET `access_token` = %s WHERE `UserID` = %s",

        # Abfrage zum Aktualisieren des Refresh-Access-Tokens
        "update_refresh_access_token": "UPDATE `user_account` SET `refresh_token` = %s WHERE `UserID` = %s",

        # Abfrage zur Auswahl des Benutzers anhand des Benutzernamens
        "select_user_by_name": "SELECT `UserID` FROM `user_account` WHERE `Username` = %s",

        # Abfrage zum Einfügen eines neuen Benutzers
        "insert_user": "INSERT INTO `user_account` (`Username`, `Password`) VALUES (%s, %s)",

        # Abfrage zum Aktualisieren von Access- und Refresh-Token
        "update_tokens": "UPDATE `user_account` SET `access_token` = %s, `refresh_token` = %s WHERE `UserID` = %s",

        # Abfrage zum Überprüfen des Refresh-Tokens
        "check_refresh_token": "SELECT count(*) as count FROM `user_account` WHERE `UserID` = %s AND `refresh_token` = %s",

        # Abfrage zum Entfernen eines Refresh-Tokens (z.B. bei Logout)
        "delete_refresh_token": "UPDATE `user_account` SET `refresh_token` = NULL WHERE `UserID` = %s"
    }
