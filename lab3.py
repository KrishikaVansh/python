import csv
import sys

def load_trains(filename):
    trains = {}
    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                trains[row['Train ID']] = {
                    "TrainName": row['Train Name'],
                    "Source": row['Source Station'],
                    "Destination": row['Destination Station'],
                    "Seats": int(row['Total Seats']),
                    "FarePerSeat": int(row['fareperseat'])
                }
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    except KeyError as e:
        print(f"CSV format error: Missing column {e}")
        sys.exit(1)
    return trains

def load_passengers(filename):
    passengers = []
    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                passengers.append({
                    "Name": row['Passenger Name'],
                    "TrainID": row['Train ID'],
                    "Tickets": int(row['Number of Tickets'])
                })
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    except KeyError as e:
        print(f"CSV format error: Missing column {e}")
        sys.exit(1)
    return passengers

def check_availability(train, requested_tickets):
    return train["Seats"] >= requested_tickets

def calculate_fare(tickets, fare_per_seat):
    return tickets * fare_per_seat

def book_ticket(trains, passenger, revenue):
    train_id = passenger["TrainID"]
    if train_id not in trains:
        print(f"Booking Error for {passenger['Name']}: Invalid Train ID {train_id}")
        return
    train = trains[train_id]
    requested_tickets = passenger["Tickets"]
    if check_availability(train, requested_tickets):
        fare = calculate_fare(requested_tickets, train["FarePerSeat"])
        train["Seats"] -= requested_tickets
        revenue[train_id] = revenue.get(train_id, 0) + fare
        print(f"Booking confirmed for {passenger['Name']} on Train {train_id} | Fare: Rs.{fare}")
    else:
        print(f"Booking Error for {passenger['Name']}: Not enough seats available.")

def generate_report1(trains):
    print("\n--- Report 1: Train Details & Seat Availability ---")
    print(f"{'Train ID':<10} {'Train Name':<20} {'Source':<15} {'Destination':<15} {'Seats Available'}")
    for tid, details in trains.items():
        print(f"{tid:<10} {details['TrainName']:<20} {details['Source']:<15} {details['Destination']:<15} {details['Seats']}")

def generate_report2(revenue, trains):
    print("\n--- Report 2: Train Revenue ---")
    print(f"{'Train ID':<10} {'Train Name':<20} {'Revenue (Rs.)'}")
    for tid, rev in revenue.items():
        print(f"{tid:<10} {trains[tid]['TrainName']:<20} {rev}")

def main():
    trains_file = "Train.csv"
    passengers_file = "Passenger.csv"
    trains = load_trains(trains_file)
    passengers = load_passengers(passengers_file)
    revenue = {}
    for passenger in passengers:
        book_ticket(trains, passenger, revenue)
    generate_report1(trains)
    generate_report2(revenue, trains)

if __name__ == "__main__":
    main()
