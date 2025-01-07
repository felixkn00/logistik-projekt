from moduls.database import Database
from mysql.connector import Error
from moduls.sql_templates import SQLTemplates

class Permissions():
    def __init__(self, UserID):
        print("Start Permissions Instance ...")
        self.create = None
        self.read = None
        self.update = None
        self.delete = None
        self.isSuperuser = None

        if UserID is None:
            raise ValueError("user_id cannot be None")
        self.UserID = UserID
        self.sql_templates_obj = SQLTemplates()

        try:
            self.database = Database(host="localhost", user="root", password="", database="logi_connect")
            self.sql_templates_obj = SQLTemplates
        except Error as e:
            print(f"Connecting Error: {str(e)}")
            self.database = None
        try:
            get_permission_query = self.sql_templates_obj.user['get_permissions']
            get_permission_data = self.database.fetch_all(get_permission_query,
                                                          (UserID,))

            print("permissions :", get_permission_data)

            if get_permission_data and len(get_permission_data[0]) >= 5:
                permissions = get_permission_data[0]
                self.create, self.read, self.update, self.delete, self.superuser = permissions[:5]
            else:
                self.create = self.read = self.update = self.delete, self.superuser = None
        except Exception as e:
            print("database error:", e)

    # can create
    def can_create(self):
        print(f"Permission create: {self.create}")
        return self.create

    # can read
    def can_read(self):
        print(f"Permission read: {self.read}")
        return self.read

    # can update
    def can_update(self):
        print(f"Permission Read: {self.update}")
        return self.update

    # can delete
    def can_delete(self):
        print(f"Permission delete: {self.delete}")
        return self.delete

    def is_superuser(self):
        print(f"Permission isSuperuser: {self.superuser}")
        return self.isSuperuser

    # return all permissions
    def get_all(self):
        return {
            "create": self.create,
            "read": self.read,
            "update": self.update,
            "delete": self.delete,
            "superuser": self.superuser
        }

    # update permissions
    def update_permissions(self, set_create, set_read, set_update, set_delete):
        update_permissions_query = self.sql_templates_obj.user['update_permissions']
        update_permissions_data = self.database.update(update_permissions_query, (set_create, set_read, set_update, set_delete,))

