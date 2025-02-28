# Author : S.M.J.K.Subasinghe
# Date : 05/12/2024
# Student ID (UoW) : 21206191
# Student ID (IIT) : 20233154

#---------------------------------------------------
# Task A - Input Validation

def validate_date_input():
    """
    - validate user input for date in DD MM YYYY format and generates the file name

    the function returns :
       > formatted_date : DD/MM/YYYY format
       > file_name : file name corresponding to the entered date in the format traffic_dateDDMMYYYY.csv
    
    """
    def validate(prompt,mini_val,max_val):
        """
        ensures the user inputs an integer within the specified range

        - prompt (str) : Message to display to the user
        - mini_val (int) : Minimum acceptable value
        - max_val (int) : Maximum acceptable value

        function returns:
        - a value - a valid integer input by the user
        
        """
        while True:
            try:
                value = int(input(prompt)) # display prompt for the user to enter a value
                if mini_val <= value <= max_val:
                    return value # check if the value is within the range
                else:
                    # display user that value not in range
                    print(f"Out of range - value must be in the range {mini_val} to {max_val}.")
            except ValueError:
                print("Integer required.") # display that the value is not an integer

    day = validate("Please enter the day of the survey in format dd : ",1,31) # the prompt, mini value and max value
    month = validate("Please enter the month of the survey in format MM : ",1,12)
    year = validate("Please enter the year of the survey in format YYYY : ",2000,2024)

    # format the date as DD/MM/YYYY 
    formatted_date = f"{day:02}/{month:02}/{year}"

    # generate the file name based on the date
    file_name = f"traffic_data{day:02}{month:02}{year}.csv"

    return formatted_date, file_name # return value in the formatted date form DD/MM/YYYY


def validate_continue():
    """
    To check if the user wants to load another dataset.

    returns:
    - str : 'Y' if the user wants to continue, 'N' if they want to stop
    
    """
    while True:
        # ask user if they want to load another dataset 
        user_input = input("Do you want to select another data file for a different date? Y/N > \nPlease enter 'Y' or 'N': ").strip().upper()
        if user_input in ["Y", "N"]:
            return user_input
        else:
            print("Invalid input. Please enter 'Y' or 'N'.") # display user'input is not valid

# ----------------------------------------------------
# Task B : Processed Outcomes

import csv

def process_csv_data(file_path):
    """
    Processes data from the CSV file for the selected dataset.

    Calculates:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Total two-wheeled vehicles
    - Buses turning north at Elm
    - Straight vehicles
    - Percentage of trucks
    - Average bicycles per hour
    - Number of speeding vehicles
    - Vehicles at Elm and Hanley junctions
    - Percentage of scooters at Elm
    - Peak traffic hours and vehicle count
    - Rainy hours

    returns:
    - dict : a dictionary of calculted values or none if file not found
    """

    # initialize variables
    total_vehicles = total_trucks = total_electric = total_2_wheel = 0
    bus_north = straight_vehicles = speeding_vehicles = 0
    elm_vehicles = hanley_vehicles = scooter_elm = rainy_hr = 0

    # dictionary to count the traffic hourly at Hanley
    hourly_traffic_hanley = {}

    # dictionary to count the traffic hourly at Elm - this is used in task d
    hourly_traffic_elm = {}

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)  # read the CSV file row by row
            # the column header from the 1st row is used as keys for the dictionary
            # data in each row is used as values for the keys
            
            for row in reader:
                total_vehicles += 1 

                if row["VehicleType"] == "Truck":
                    total_trucks += 1

                if row["elctricHybrid"] == "TRUE":   # check if vehicle is an electric hybrid
                    total_electric += 1 

                if row["VehicleType"] in ["Bike", "Motorbike", "Scooter"]:
                    total_2_wheel += 1 # count all the vehicles that are 2 wheeled

                if row["VehicleType"] == "Scooter" and "Elm Avenue" in row["JunctionName"]:
                    scooter_elm += 1 # count the number of scooter at Elm Junction
                    
                # count the number of bus going North
                if row["VehicleType"] == "Bus" and row["travel_Direction_out"] == "N" and "Elm Avenue" in row["JunctionName"]:
                    bus_north += 1

                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    straight_vehicles += 1 # vehicles going straight - no turning

                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    speeding_vehicles += 1
                    # vehicle speed greater than speed limit

                if "Elm Avenue" in row["JunctionName"]: # count number of vehicles at Elm junction
                    elm_vehicles += 1
                    hour = int(row["timeOfDay"].split(":")[0]) # get the hour from timeOfDay
                    hourly_traffic_elm[hour] = hourly_traffic_elm.get(hour, 0) + 1

                if "Hanley Highway" in row["JunctionName"]:
                    hanley_vehicles += 1 # count number of vehicles at Hanley
                    hour = int(row["timeOfDay"].split(":")[0]) # get hour from timeOfDay
                    hourly_traffic_hanley[hour] = hourly_traffic_hanley.get(hour, 0) + 1
                    
                    """
                    Count Vehicles for Each Hour:

                     >  A dictionary named hourly_traffic_hanley keeps track the total vehicle count for each hour.
                     
                     > The get() method is used to retrieve the existing count for that hour (if any)
                     or default to 0 if it’s the first vehicle for that hour. Then, it adds 1 to the count.

                     """

                # count number of hours it rained
                if row["Weather_Conditions"] == "Rain":
                    rainy_hr += 1

        #get the peak traffic hours on Hanley
        peak_traffic = max(hourly_traffic_hanley.values(), default=0) # get max traffic in any hour
            # default=0 ensures :
            
            # if there are no traffic records (empty dictionary), the result is 0 to avoid errors.
        
        peak_hours = [
            f"{hour}:00-{hour + 1}:00"
            for hour, count in hourly_traffic_hanley.items()
            if count == peak_traffic
        ]
        # the peak_hour found by:
        # > looping through all hours using hourly_traffic_hanley.items() - there the values are stored as (hour, count).
        # > then check if the count for the hour matches peak_traffic, if it matches - then selected as peak hour
        # > each hour is dispalyed as (hour:00-hour:00)

        # calculate % of trucks
        truck_percent = round((total_trucks / total_vehicles) * 100) if total_vehicles else 0
                         # round() - rounded to the nearest whole number
                         
        # calculate % of scooters at Elm
        scooters_percent = round((scooter_elm / total_vehicles) * 100) if total_vehicles else 0

        # calculate the average number of bicycles per hour
        avg_bicycles_per_hour = round(total_2_wheel / 24) if total_2_wheel else 0

        # Return all results as a dictionary
        return {
            "File": file_path,
            "Total vehicles": total_vehicles,
            "Total trucks": total_trucks,
            "Total electric vehicles": total_electric,
            "Total two-wheeled vehicles": total_2_wheel,
            "Buses turning north at Elm": bus_north,
            "Straight vehicles": straight_vehicles,
            "Truck percentage": f"{truck_percent}%",
            "Average bicycles per hour": avg_bicycles_per_hour,
            "Speeding vehicles": speeding_vehicles,
            "Elm junction vehicles": elm_vehicles,
            "Hanley junction vehicles": hanley_vehicles,
            "Scooters percentage at Elm": f"{scooters_percent}%",
            "Peak traffic count": peak_traffic,
            "Peak hours": ", ".join(peak_hours),
            "Rainy hours": rainy_hr,
            "Hourly traffic at Elm" : hourly_traffic_elm,
            "Hourly traffic at Hanley": hourly_traffic_hanley,
        }

    except FileNotFoundError:
        # if file not found - print an error message
        print(f"Error: File '{file_path}' not found.")
        return None # as there is no data to process
# -----
def display_results(results):
    """
    displays the processed results from task B in a formatted output
    """
    # Printing the header
    print("\n" + "*" * 27)
    print(f"data file selected is {results['File']}")
    print("*" * 27)

    # dispay the Total vehicles, Total trucks, Total electric, Total 2wheeled, Buses going north, Straight vehicles, % trucks, Average bicycles per hour
    print()
    print(f"The total number of vehicles recorded for this date is {results['Total vehicles']}")
    print(f"The total number of trucks recorded for this date is {results['Total trucks']}")
    print(f"The total number of electric vehicles for this date is {results['Total electric vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {results['Total two-wheeled vehicles']}")
    print(f"The total number of Buses leaving Elm Avenue/Rabbit Road heading North is {results['Buses turning north at Elm']}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {results['Straight vehicles']}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {results['Truck percentage']}")
    print(f"The average number of Bikes per hour for this date is {results['Average bicycles per hour']}\n")

    # display Over-speeding and Junction Statistics
    print(f"The total number of Vehicles recorded as over the speed limit for this date is {results['Speeding vehicles']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {results['Elm junction vehicles']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {results['Hanley junction vehicles']}")
    print(f"The percentage of scooters through Elm Avenue/Rabbit Road is {results['Scooters percentage at Elm']}\n")

    #  display traffic and Weather Insights
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {results['Peak traffic count']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded at {results['Peak hours']}")
    print(f"The number of hours of rain for this date is {results['Rainy hours']}")
    print()

def save_results_to_file(results,file_name = "results.txt"):
    '''
    save the processed outcome got from task B to a text file and appends if the program loops

    - results (dict)  : processed data to save
    - file_name (str) : Name of the text file to save results to
    
    '''
    with open(file_name,"a")as file:
        for key, value in results.items():
                file.write(f"{key}: {value}\n")
        file.write("\n")
    print(f"Results saved to {file_name}")
    print()


# Task D: Histogram

import tkinter as tk

class HistogramApp:
    def __init__(self, root, traffic_data, date):
        self.root = root
        self.traffic_data = traffic_data
        self.date = date # date the histogram is made for
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        self.draw_histogram() # used to draw the chart

        # root - the main tkinter window
        # traffic_data - a dictionary that is holding the traffic data for both roads

        # canvas = a blank drawing area of size 800x600 is initialized with a white background

    def draw_histogram(self):
        self.canvas.delete("all") # any old drawing on the canvas are erased

        # Title of the histogram 
        self.canvas.create_text(400, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 16), fill="black")

        # Legend -  shows the colors of the bars and what the represent
        self.canvas.create_rectangle(650, 50, 670, 70, fill="blue")
        self.canvas.create_text(680, 60, text="Elm Avenue", anchor="w", font=("Arial", 10))

        self.canvas.create_rectangle(650, 80, 670, 100, fill="green")
        self.canvas.create_text(680, 90, text="Hanley Highway", anchor="w", font=("Arial", 10))

        # X-axis and Y-axis labels
        self.canvas.create_line(50, 550, 750, 550, fill="black", width=2)  # X-axis 
        # self.canvas.create_line(50, 550, 50, 50, fill="black", width=2)  # Y-axis
            # - its commented to make the histogram look like the one given in the coursework specification

        for i in range(24):  # Hour markers
            x = 50 + (i * 30)
            self.canvas.create_text(x, 560, text=f"{i}:00", font=("Arial", 8))
            # for each hour i, the x-coordinate shifts by 30 pixels, starting from 50.
            # just to make an organized layout for the bars on the x-axis.


        # Traffic data normalization for bar heights
        max_count = max(max(self.traffic_data["Elm"].values()), max(self.traffic_data["Hanley"].values()))
        # gets the max vehicle count from both sides
        scaling_factor = 400 / max_count if max_count else 1
        # to make sure that the tallest bar fits within 400 pixels
        # If max_count is 0 (no data), the factor defaults to 1 - cant divide by 0

        # Drawing bars
        for hour in range(24):
            x = 50 + (hour * 30)
            
            # Elm Avenue bar
            elm_count = self.traffic_data["Elm"].get(hour, 0)
            elm_height = elm_count * scaling_factor
            self.canvas.create_rectangle(x - 10, 550 - elm_height, x, 550, fill="blue")
            self.canvas.create_text(x - 5, 550 - elm_height - 10, text=str(elm_count), font=("Arial", 8), fill="blue") # display the count on top the bar
            

            # Hanley Highway bar
            hanley_count = self.traffic_data["Hanley"].get(hour, 0)
            hanley_height = hanley_count * scaling_factor
            self.canvas.create_rectangle(x, 550 - hanley_height, x + 10, 550, fill="green")
            self.canvas.create_text(x + 10, 550 - hanley_height - 10, text=str(hanley_count), font=("Arial", 8), fill="green") # display the count on top the bar

# Task E: Main Program with Loop
def main_loop():
    """
    Main loop for the program to allow users to process multiple datasets until they choose to stop.
    """
    while True:
        # Validate date and get the corresponding file name - task A
        formatted_date, file_name = validate_date_input()

        # Process the CSV data for the given file - task B
        results = process_csv_data(file_name)
        if results:
            # Display the results - task B
            display_results(results)

            # Optionally save results to a file - task C
            save_results_to_file(results)

            # get the traffic data for the histogram to use - took data from task B
            traffic_data = {
                "Elm": {hour:results.get("Hourly traffic at Elm",{}).get(hour,0) for hour in range(24)},
                "Hanley": {hour:results.get("Hourly traffic at Hanley",{}).get(hour,0) for hour in range(24)},
                }

            # display the histogram - task D
            root = tk.Tk()
            root.title("Traffic Data Histogram")
            app = HistogramApp(root, traffic_data, formatted_date)
            root.mainloop()

        # Check if the user wants to load another dataset - task A
        user_choice = validate_continue()
        if user_choice.strip().upper() == 'N':
            print("End of run")
            break
            

if __name__ == "__main__":
    main_loop()


