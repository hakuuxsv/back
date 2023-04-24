import requests
from bs4 import BeautifulSoup
import json

def retrieve_daily_lessons(start_idx, end_idx, table_rows):
    daily_lessons = []
    for idx in range(start_idx, end_idx):
        if idx == start_idx:
            cell_idx = 28
        else:
            cell_idx = 27

        lesson_entry = " ".join(table_rows[idx].find_all("td")[cell_idx].text.split())

        if not lesson_entry:
            lesson_entry = "Нет пары"
        daily_lessons.append(lesson_entry)
    return daily_lessons

source_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-Qk-0tbwz8BbZ9OZsLk3fJHOny7cs491VQanDGnNq_06fMFlvr2WNb6D7am6KCQ73BMyCWMk66kdU/pubhtml"
response_data = requests.get(source_url)
soup_content = BeautifulSoup(response_data.content, "html.parser")
table_rows = soup_content.find("tbody").find_all("tr")

schedule_data = {}

start_day_idx = 5
day_indices = {}

for idx in range(start_day_idx, start_day_idx + 20, 4):
    day_of_week = table_rows[idx].find_all("td")[0].text.strip()
    day_indices[day_of_week] = (idx, idx + 4)

for day in day_indices:
    start_idx, end_idx = day_indices[day]
    lessons = retrieve_daily_lessons(start_idx, end_idx, table_rows)
    schedule_data[day] = lessons

with open("schedule_data.json", "w", encoding="utf-8") as json_file:
    json.dump(schedule_data, json_file, indent=4, ensure_ascii=False)

with open("schedule_data.txt", "w", encoding="utf-8") as txt_file:
    for day, lessons_list in schedule_data.items():
        txt_file.write(f"{day}:\n")
        txt_file.write("\n".join(lessons_list) + "\n\n")