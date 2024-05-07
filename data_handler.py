import json
import os
from datetime import datetime
import shutil
from pathlib import Path
import copy
from typing import Union
import random


class DataHandler:

    save_file_name = "data.json"
    backup_folder_name = "backups"
    detail_icon_location = "data/detail_icons"

    base_data_structure = {
        "settings": {
            "detail_icon_location": detail_icon_location,
            "detail_icons": {
                "primary_email": {"display_name": "E-Mail", "img": "email.png"},
                "password": {"display_name": "Password", "img": "password.png"},
                "unknown_detail": {"display_name": "Unknown Detail", "img": "unknown_detail.png"},
            }
        },
        "infos": {
            "next_id": 0,
            "next_group_id": 0
        },
        "accounts": {
            # Accounts will be saved here
        },
        "groups": {
            # Group attributes will be saved here
        }
    }

    def __init__(self, save_file_location):
        self.save_file_location = save_file_location
        self.save_file_path = os.path.join(self.save_file_location, DataHandler.save_file_name)
        self.data = {}

        # Check integrity of save file and create new one if corrupted
        if not self.validate_save_file():
            self.backup_save_file(prefix="BACKUP_FAILED_VALIDATION_")
            self.create_save_file()

        self.read_save_file()

    def read_save_file(self):
        """
        Read save file at class instance defined location
        """

        print(f"Loading data from {self.save_file_path}...", end="")

        # Try reading save file
        try:
            with open(self.save_file_path) as json_file:
                data = json.load(json_file)
                print(f"done -> {len(data['accounts'])} account{'s' if len(data['accounts']) != 1 else ''} loaded.")
                self.data = data
                return True

        except Exception as e:
            print(f"failed. {e}")
            return False

    def validate_save_file(self):
        """
        Validates save file. Currently only checks if all root keys of the base structure exist
        """

        print(f"Validating save file...", end="")

        # Start validation
        try:
            with open(self.save_file_path) as json_file:
                data = json.load(json_file)

                # Check key integrity
                for key in DataHandler.base_data_structure.keys():
                    # CASE: Base key not present in save file
                    if key not in data.keys():
                        print("failed. File corrupted!")
                        return False

                # CASE: All checks passed
                print("done.")
                return True

        # CASE: File could not be read or unknown error
        except Exception as e:
            print(f"failed. {e}")
            return False

    def create_save_file(self):
        """
        Creates new savefile at class default path with default base structure
        """

        print("Creating new save file...", end="")

        # Try creating the save file
        try:
            with open(self.save_file_path, 'w') as json_file:
                json.dump(DataHandler.base_data_structure, json_file, indent=4)
            print("done.")
            return True

        except Exception as e:
            print(f"failed. {e}")
            return False

    def backup_save_file(self, prefix: str = "BACKUP_", backup_location: Path = None):
        """
        Creates a copy of the current save file at a specified location.
        :param prefix: Pefix of the backup file name. Will be followed by the date and time
        :param backup_location: Path in which the backup will be created
        """

        # Define default backup location if not specified
        if backup_location is None:
            backup_location = os.path.join(self.save_file_location, DataHandler.backup_folder_name)

        # Define path for and backup file
        backup_file_name = prefix + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json"
        backup_file_path = os.path.join(backup_location, backup_file_name)

        print(f"Backing up save file to {backup_location}...", end="")

        # Try copying file
        try:
            shutil.copyfile(self.save_file_path, backup_file_path)
            print("done.")
            return True

        except Exception as e:
            print(f"failed. {e}")
            return False

    def update_save_file(self):
        """
        Save current data structure to save file
        """

        print("Updating save file...", end="")

        # Try updating the save file
        try:
            with open(self.save_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
            print("done.")
            return True

        except Exception as e:
            print(f"failed. {e}")
            return False

    def add_account(self, account_details: dict, account_name: str, group_id: Union[None, int, str] = None, save_to_file=True):
        """
        Add an account to the save file
        :param account_details: Parameters of the account
        :param group_id: ID of group of the account. If None, account is in no group
        :param save_to_file: Specify if changes are saved directly to file
        """

        # Store the original state in case of roll back
        original_data = copy.deepcopy(self.data)

        try:
            # Add new account
            new_account_id = str(self.data["infos"]["next_id"])
            self.data["accounts"][new_account_id] = account_details

            # Add metadata
            self.data["accounts"][new_account_id]["group_id"] = str(group_id)
            self.data["accounts"][new_account_id]["account_name"] = str(account_name)

            # Increment id
            self.data["infos"]["next_id"] += 1

            # Save changes to file
            if save_to_file:
                self.update_save_file()

            print(f"Added new account with ID={new_account_id}.")

        except Exception as e:
            # Roll back to original state in case of error
            self.data = original_data
            print(f"Failed to add account. {e}")
            return False

        return True

    def delete_account(self, account_id, save_to_file=True):
        """
        Delete an account
        :param account_id: Id of the account
        :param save_to_file: Specify if changes are saved directly to file
        """

        # Store the original state in case of roll back
        original_data = copy.deepcopy(self.data)

        try:
            # Delete account
            del self.data["accounts"][str(account_id)]

            # Save changes to file
            if save_to_file:
                self.update_save_file()

            print(f"Deleted account with ID={account_id}.")

        except Exception as e:
            print(self.data["accounts"].keys())
            # Roll back to original state in case of error
            self.data = original_data
            print(f"Failed to delete account. {e}")
            return False

        return True

    def update_account(self, account_id: Union[int, str], updated_parameters: dict, save_to_file: bool = True):
        """
        Update an existing account
        :param account_id: Id of the account
        :param updated_parameters: Dictionary of parameters. Existing keys will get updated.
        For new keys new key value pair will be created. Keys with None as value will get deleted
        :param save_to_file: Specify if changes are saved directly to file
        """

        # Store the original state in case of roll back
        original_data = copy.deepcopy(self.data)

        try:

            updates, deletions = 0, 0

            # Update/Delete defined parameters
            for key, value in updated_parameters.items():
                if value is not None:
                    self.data["accounts"][str(account_id)][key] = value
                    updates += 1
                else:
                    del self.data["accounts"][str(account_id)][key]
                    deletions += 1

            # Save changes to file
            if save_to_file:
                self.update_save_file()

            print(f"Updated account with ID={account_id} -> {updates} parameter{'s' if updates != 1 else ''} updated, "
                  f"{deletions} parameter{'s' if deletions != 1 else ''} deleted.")

        except Exception as e:
            print(self.data["accounts"].keys())
            # Roll back to original state in case of error
            self.data = original_data
            print(f"Failed to update account. {e}")
            return False

        return True

    def add_group(self, name, save_to_file: bool = True):
        """
        Add a group to the save file
        :param name: name of the group
        :param save_to_file: Specify if changes are saved directly to file
        """

        # Store the original state in case of roll back
        original_data = copy.deepcopy(self.data)

        try:
            # Add new group
            new_group_id = str(self.data["infos"]["next_group_id"])
            self.data["groups"][str(new_group_id)] = {"name": name}

            # Increment id
            self.data["infos"]["next_group_id"] += 1

            # Save changes to file
            if save_to_file:
                self.update_save_file()

            print(f"Added new group with ID={new_group_id}.")

        except Exception as e:
            # Roll back to original state in case of error
            self.data = original_data
            print(f"Failed to add group. {e}")
            return False

        return True

    def dev_only_create_dummy_data(self, num=50):
        self.create_save_file()
        self.read_save_file()

        self.add_group("Emails")
        self.add_group("Services")
        self.add_group("Shopping")

        words = ["cat", "secret", "football", "mystery", "travel", "coding", "adventure", "music", "art", "science"]
        providers = ["google", "amazon", "twitter", "aws", "reddit", "ikea", "microsoft", "apple", "netflix", "spotify"]
        dividers = [".", "_", "-"]
        domains = ["com", "de", "net"]

        generated_mails = []

        def random_mail():
            new_mail = (random.choice(dividers).join([random.choice(words) for _ in range(random.randint(1, 3))]) +
                        "@" + random.choice(providers) + "." + random.choice(domains))
            generated_mails.append(new_mail)
            return new_mail

        def random_password():
            return str(random.choice([random.randint(0, 99)])).join([random.choice(words) for _ in range(random.randint(1, 3))])


        for _ in range(int(num/4)):
            self.add_account({"primary_email": random_mail(),
                              "password": random_password(),
                              "address": "street 0\nplz city\ncountry",
                              "phone": random.randint(100000000, 999999999)}
                             , account_name=random.choice(providers).capitalize(), group_id=0, save_to_file=False)

        for _ in range(int(num/2)):
            self.add_account({"primary_email": random.choice(generated_mails),
                              "password": random_password()}
                             , account_name=random.choice(providers).capitalize(), group_id=1, save_to_file=False)

        for _ in range(int(num/2)):
            self.add_account({"primary_email": random.choice(generated_mails),
                              "password": random_password()}
                             , account_name=random.choice(providers).capitalize(), group_id=2, save_to_file=False)

        self.update_save_file()


if __name__ == '__main__':

    dh = DataHandler(save_file_location="data")
    dh.create_save_file()
    dh.read_save_file()

    for i in range(3):
        dh.add_account({"primary_email": f"debug_email_{random.randint(0, 100)}",
                        "password": f"debug_password_{random.randint(0, 100)}",
                        "address": "street 0\nplz city\ncountry",
                        "phone": random.randint(100000000, 999999999)}
                       , save_to_file=False)

    dh.update_save_file()
    dh.delete_account(0)

    dh.update_account(1, {"password": "new_password", "new_parameter": "new_value", "phone": None})
