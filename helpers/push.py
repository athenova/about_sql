
from datetime import datetime
from datetime import timedelta
import json
import os

TOPIC_WORD_LIMIT = 300

tasks_file = 'files/in_progress.json'
backlog_file = 'files/backlog.json'

if not os.path.exists(tasks_file):
    if os.path.exists(backlog_file):
        tasks = json.load(open(backlog_file, "rt", encoding="UTF-8"))
        index_start = max(tasks, key=lambda task: task['index'])['index'] + 1
    else:
        tasks = []
        index_start = 1
    for root, dirs, files in os.walk('files/new'):
        for i, file in enumerate(files):
            input_file = f"{root}/{file}"
            data = json.load(open(input_file, "rt", encoding="UTF-8"))
            for item in data:
                task = { 
                    "index": i + index_start,
                    "domain": item['domain'],
                    "name": item['problem'],
                    "description_prompt": f"Опиши проблему '{item['problem']}' связанную с технологией '{item['technology']}' и программным средством '{item['soft']}' из области '{item['domain']}', не описывай решение, используй не более {TOPIC_WORD_LIMIT} слов",
                    "solution_prompt": f"Опиши решение проблемы '{item['problem']}' связанной с технологией '{item['technology']}' и программным средством '{item['soft']}' из области '{item['domain']}', используй не более {TOPIC_WORD_LIMIT} слов",
                    "group": f"{item['technology']}/{item['soft']}",
                }
                tasks.append(task)
            processed_file = f"files/processed/{file}"
            os.rename(input_file, processed_file)

    curr_date = datetime.today() + timedelta(days=8)
    for task in tasks:
        task["date"] = curr_date.strftime("%Y-%m-%d")
        curr_date += timedelta(days=7)

    json.dump(tasks, open(tasks_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)
    if os.path.exists(backlog_file):
        os.remove(backlog_file)
    print(f"{len(tasks)} tasks created")
else: 
    print("Tasks already exists, revert before push")