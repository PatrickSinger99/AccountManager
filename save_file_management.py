import json


"""CLASS SAVE FILE"""


class SaveFile:
    def __init__(self):
        # Parameters
        self.save_file_location = "saved_data.json"
        self.save_data = {}

        # Try to load save file. If not possible, create new save file.
        try:
            self.load_save_file()
            print("[INFO] Loaded data from save file.")
        except FileNotFoundError:
            print("[WARNING] Could not find save file.")
            self.create_new_save_file()

    # Load data from save file into class variable "self.save_data".
    def load_save_file(self):

        with open(self.save_file_location, "r") as save_file:
            save_data = json.load(save_file)
            self.save_data = save_data

    # Create new save file.
    def create_new_save_file(self):
        try:
            save_structure = {"e_mail_accounts": [], "service_accounts": []}

            json_object = json.dumps(save_structure, indent=4)

            with open(self.save_file_location, "w") as new_save_file:
                new_save_file.write(json_object)

            print("[INFO] Created new save file.")

        except:
            print("[ERROR] Failed to create new save file.")

    # Update save file with data from class variable "self.save_data".
    def update_save_file(self):
        try:
            json_object = json.dumps(self.save_data, indent=4)

            with open(self.save_file_location, "w") as new_save_file:
                new_save_file.write(json_object)

        except:
            print("[ERROR] Failed to update save file.")

    # Add new account to save file.
    def add_new_account(self, account_name, e_mail="", password="", username="", name="", safety_question="",
                        birthdate="", address="", mobile_number="", pin="", second_e_mail="", third_e_mail="", code="",
                        additional_information="", is_email_account=False):
        try:
            # Refresh save data.
            self.load_save_file()

            new_account_dict = {"id": self.get_next_id(),
                                "account_name": account_name,
                                "e_mail": e_mail,
                                "password": password,
                                "username": username,
                                "name": name,
                                "safety_question": safety_question,
                                "birthdate": birthdate,
                                "address": address,
                                "mobile_number": mobile_number,
                                "pin": pin,
                                "second_e_mail": second_e_mail,
                                "third_e_mail": third_e_mail,
                                "code": code,
                                "additional_information": additional_information,
                                "is_email_account": is_email_account}

            # Add new account to save data.
            if is_email_account:
                self.save_data["e_mail_accounts"].append(new_account_dict)
            else:
                self.save_data["service_accounts"].append(new_account_dict)

            # Update save file with new version.
            self.update_save_file()
            print("[INFO] Added " + account_name + " account.")

        except:
            print("[ERROR] Could not add " + account_name + " account.")

    # Delete account with ID.
    def delete_account(self, account_id):
        try:
            # Refresh save data.
            self.load_save_file()
            found = False

            for account in self.save_data["e_mail_accounts"]:
                if account["id"] == account_id:
                    self.save_data["e_mail_accounts"].remove(account)
                    found = True
                    break

            if not found:
                for account in self.save_data["service_accounts"]:
                    if account["id"] == account_id:
                        self.save_data["service_accounts"].remove(account)
                        found = True
                        break

            if found:
                self.update_save_file()
                print("[INFO] Deleted " + account["account_name"] + " account.")
            else:
                print("[ERROR] Could not find account with ID " + str(account_id) + ".")

        except:
            print("[ERROR] Failed to delete account.")

    # Get next ID value.
    def get_next_id(self):
        highest_id = -1

        for account in self.save_data["e_mail_accounts"] + self.save_data["service_accounts"]:
            if account["id"] > highest_id:
                highest_id = account["id"]

        return highest_id + 1

    # Print all stored data
    def print_saved_data(self):
        print()
        for category in self.save_data:
            print(category + "\n" + "-"*len(category))
            for account in self.save_data[category]:
                for info in account:
                    if account[info] != "" and info != "is_email_account":
                        print(info + ": " + str(account[info]))
                print()
            print()

    # Print all stored data compacted
    def print_compact_saved_data(self):
        print()
        for category in self.save_data:
            print(category + "\n" + "-"*len(category))
            for account in self.save_data[category]:
                print("[" + str(account["id"]) + "] " + account["account_name"])
            print()


if __name__ == "__main__":
    s1 = SaveFile()
    s1.create_new_save_file()

    s1.add_new_account("Google", password="sussy", e_mail="butterdog@gmail.com", is_email_account=True)
    s1.add_new_account("Web.de", password="123patlol", e_mail="fortnitegangster@web.de", is_email_account=True)
    s1.add_new_account("Amazon", password="123lol", e_mail="butterdog@gmail.com")
    s1.add_new_account("Linked In", password="abc123.", e_mail="butterdog@gmail.com")
    s1.add_new_account("Reddit", password="amogus", e_mail="fortnitegangster@web.de")

    s1.delete_account(2)
    s1.print_compact_saved_data()

