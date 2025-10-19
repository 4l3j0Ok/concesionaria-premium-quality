import os
import requests
import json


def populate_mocked_cars():
    host = os.getenv("APP_HOST", "localhost")
    port = int(os.getenv("APP_PORT", 8000))
    url = f"http://{host}:{port}/cars/"
    headers = {"Content-Type": "application/json"}
    with open("cars.json", "r") as file:
        mocked_cars = json.load(file)
    for car in mocked_cars:
        response = requests.post(url, json=car, headers=headers)
        if response.status_code == 201:
            print(f"Car {car['brand']} {car['model']} created successfully.")
        else:
            print(
                f"Failed to create car {car['brand']} {car['model']}. Status code: {response.status_code}, Response: {response.text}"
            )


if __name__ == "__main__":
    populate_mocked_cars()
