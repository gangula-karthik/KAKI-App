import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../Account_management/credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})


def count_signups_per_year_month(year, month):
    users_data = db.reference("/Users/Consumer").get()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    month_index = months.index(month)

    year_month_counts = []

    for i in range(6):
        current_month_index = (month_index - i) % 12
        current_month = months[current_month_index]
        current_year = year

        if current_month_index > month_index:
            current_year -= 1

        signups_count = 0

        if users_data:
            for user_key, user in users_data.items():
                if "year" in user and "month" in user:
                    if user["year"] == current_year and user["month"] == current_month:
                        signups_count += 1

        year_month_counts.insert(0, signups_count)  # Insert at the beginning to reverse the order

    return year_month_counts


if __name__ == "__main__":
    target_year = 2023
    target_month = "August"
    last_six_months_counts = count_signups_per_year_month(target_year, target_month)
    print(f"Last 6 months' sign-up counts starting from {target_month} {target_year}:", last_six_months_counts)