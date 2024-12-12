import os

def read_states(file_path):

    state_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            full_name, abbreviation = line.strip().split(", ")
            state_dict[abbreviation.upper()] = full_name.title()
            state_dict[full_name.title()] = full_name.title()
    return state_dict


def read_weather_files(folder_path, state_dict):

    weather_data = {}
    files = [
        "cities_weather_part1.txt",
        "cities_weather_part2.txt",
        "cities_weather_part3.txt",
        "cities_weather_part4.txt",
    ]
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    city, state, temp, humidity = [x.strip() for x in line.split(",")]
                    temp = float(temp.split()[0])
                    humidity = float(humidity.rstrip('%'))
                    state_full = state_dict.get(state.upper(), state_dict.get(state.title(), None))
                    if state_full:
                        if state_full not in weather_data:
                            weather_data[state_full] = {"temperatures": [], "humidities": []}
                        weather_data[state_full]["temperatures"].append(temp)
                        weather_data[state_full]["humidities"].append(humidity)
    return weather_data


def calculate_weather_statistics(weather_data):

    weather_stats = {}
    for state, data in weather_data.items():
        temps = data["temperatures"]
        humids = data["humidities"]
        weather_stats[state] = {
            "MaxTemperature": max(temps),
            "MinTemperature": min(temps),
            "AverageTemperature": sum(temps) / len(temps),
            "MaxHumidity": max(humids),
            "MinHumidity": min(humids),
            "AverageHumidity": sum(humids) / len(humids),
        }
    return weather_stats


def show_weather_information(states, weather_stats, state_dict):

    normalized_states = []
    for state in states:
        state_key = state.strip()
        normalized_state = state_dict.get(state_key.upper(), state_dict.get(state_key.title(), state_key))
        normalized_states.append(normalized_state)

    states_with_data = []
    states_without_data = []

    for state in normalized_states:
        if state in weather_stats:
            states_with_data.append(state)
        else:
            states_without_data.append(state)

    print("\nWeather Information:")
    print(f"{'State':<15}{'Max Temp (F)':<15}{'Min Temp (F)':<15}{'Avg Temp (F)':<15}"
          f"{'Max Hum (%)':<15}{'Min Hum (%)':<15}{'Avg Hum (%)':<15}")

    for state in states_with_data:
        stats = weather_stats[state]
        print(f"{state:<15}{stats['MaxTemperature']:<15.2f}{stats['MinTemperature']:<15.2f}"
              f"{stats['AverageTemperature']:<15.2f}{stats['MaxHumidity']:<15.2f}"
              f"{stats['MinHumidity']:<15.2f}{stats['AverageHumidity']:<15.2f}")

    for state in states_without_data:
        print(f"{state:<15}{'No data available':<15}")


def main():

    folder_path = "weather_data"
    state_file = "us_states.txt"

    state_dict = read_states(state_file)
    weather_data = read_weather_files(folder_path, state_dict)

    weather_stats = calculate_weather_statistics(weather_data)

    user_input = input("Enter states (full name or abbreviation, separated by commas): ")
    states = [state.strip() for state in user_input.split(",")]

    show_weather_information(states, weather_stats, state_dict)

main()

def read_states(file_path):
    file = open(file_path)
    text = file.readlines()
    int_state = []
    state = []
    for line in text:
        text_split = line.split(", ")
        int_state.append(text_split[1][0:2])
        state.append(text_split[0])
    dict = {}
    for i in range(len(int_state)):
        dict[int_state[i]] = state[i]

    return dict