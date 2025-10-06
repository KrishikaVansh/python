import os
import json

def read_json_files(directory):
   
    covid_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        covid_data.append(data)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return covid_data


def process_covid_data(covid_data):
    
    summary = {}

    for record in covid_data:
        country = record["country"]
        confirmed_total = record["confirmed_cases"]["total"]
        deaths_total = record["deaths"]["total"]
        recovered_total = record["recovered"]["total"]

        if country not in summary:
            summary[country] = {
                "total_confirmed": 0,
                "total_deaths": 0,
                "total_recovered": 0
            }

       
        summary[country]["total_confirmed"] += confirmed_total
        summary[country]["total_deaths"] += deaths_total
        summary[country]["total_recovered"] += recovered_total

  
    for country, stats in summary.items():
        stats["total_active"] = stats["total_confirmed"] - (
            stats["total_deaths"] + stats["total_recovered"]
        )

    return summary


def find_extremes(summary):
    
    sorted_countries = sorted(summary.items(), key=lambda x: x[1]["total_confirmed"], reverse=True)

    top_5_highest = sorted_countries[:5]
    top_5_lowest = sorted_countries[-5:]

    return top_5_highest, top_5_lowest


def save_summary(summary, output_file="covid19_summary.json"):
   
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"Summary report saved to {output_file}")


if __name__ == "__main__":
    directory = "covid_data"  
    covid_data = read_json_files(directory)
    summary = process_covid_data(covid_data)

    print("\n--- COVID-19 Statistics by Country ---")
    for country, stats in summary.items():
        print(f"{country}: {stats}")

   
    top_highest, top_lowest = find_extremes(summary)

    print("\nTop 5 countries with highest confirmed cases:")
    for country, stats in top_highest:
        print(f"{country}: {stats['total_confirmed']}")

    print("\nTop 5 countries with lowest confirmed cases:")
    for country, stats in top_lowest:
        print(f"{country}: {stats['total_confirmed']}")

   
    save_summary(summary)
