import requests
from datetime import datetime
import openpyxl


class LicenseAuthority:
    def __init__(self):
        self.base_url = "http://localhost:30000"

    def fetch_license_data(self):
        # Fetch data from the API using requests package
        url = f"{self.base_url}/drivers-licenses/list"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data from the API.")
            return []

    def list_suspended_licenses(self, data):
        # Method to list suspended licenses
        sus_licenses = [lic for lic in data if license["suspended"]]
        return sus_licenses

    def extract_valid_licenses(self, data):
        # Method to extract valid licenses issued until today's date
        today = datetime.today().strftime("%Y-%m-%d")
        val_licenses = [lic for lic in data if lic["data_de_expirare"] >= today]
        return val_licenses

    def find_license_count_by_category(self, data):
        # Create a license_count dictionary to save frequency of every category
        license_count = {}
        for lic in data:
            category = lic["categorie"]
            if category in license_count:
                license_count[category] += 1
            else:
                license_count[category] = 1
        return license_count

    def generate_excel_file(self, data, filename):
        # Generate Excel file to store generated data
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Write data to Excel sheet (Create a enumeration to use row)
        for row, lic in enumerate(data, start=1):
            sheet.append(list(lic.values()))

        # Save Excel file
        workbook.save(filename)


if __name__ == "__main__":
    authority = LicenseAuthority()
    data = authority.fetch_license_data()

    while True:
        print("Choose an option:")
        print("1. List suspended licenses")
        print("2. Extract valid licenses issued until today's date")
        print("3. Find licenses based on category and their count")
        print("4. Stop the program")

        operation_id = input("[TASK]: Enter operation ID: ")

        if operation_id == "4":
            print("[INFO]: Exiting the program...")
            break

        try:
            operation_id = int(operation_id)
            if operation_id < 1 or operation_id > 3:
                raise ValueError
        except ValueError:
            print("[ERROR]: Invalid operation ID. Please enter a number between 1 and 4.")
            continue

        file_name = input("Enter the file name (without extension): ")

        if operation_id == 1:
            suspended_licenses = authority.list_suspended_licenses(data)
            authority.generate_excel_file(suspended_licenses, f"{file_name}.xlsx")
            print(f"[INFO]: Suspended licenses data exported to {file_name}.xlsx")
        elif operation_id == 2:
            valid_licenses = authority.extract_valid_licenses(data)
            authority.generate_excel_file(valid_licenses, f"{file_name}.xlsx")
            print(f"[INFO]: Valid licenses data exported to {file_name}.xlsx")
        elif operation_id == 3:
            license_count_by_category = authority.find_license_count_by_category(data)
            license_count_data = [{"Category": category, "Count": count}
                                  for category, count in license_count_by_category.items()]
            authority.generate_excel_file(license_count_data, f"{file_name}.xlsx")
            print(f"[INFO]: License count by category data exported to {file_name}.xlsx")

