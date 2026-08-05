from utilities.csv_reader import read_login_data

data = read_login_data("testdata/login.csv")

for row in data:
    print(row)
    