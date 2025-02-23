import os
import json
import glob

from openai import OpenAI

AI_TEXT_MODEL = 'chatgpt-4o-latest'

def gen_text(task):
    folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    folder_name = glob.escape(f"{folder_name}/{task['name'].replace('/', ',')}")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    problem_file_name = f"{folder_name}/problem.txt"
    solution_file_name = f"{folder_name}/solution.txt"

    client = OpenAI()
    if not os.path.exists(problem_file_name):
        text_prompt = task["description_prompt"]
        text = client.chat.completions.create(
                    model=AI_TEXT_MODEL,
                    messages=[
                        { "role": "system", "content": f"Ты - архитектор решений" },
                        { "role": "user", "content": text_prompt },
                    ]
                ).choices[0].message.content
        open(problem_file_name, 'wt', encoding="UTF-8").write(text)

    if not os.path.exists(solution_file_name):
        text_prompt = task["solution_prompt"]
        text = client.chat.completions.create(
                    model=AI_TEXT_MODEL,
                    messages=[
                        { "role": "system", "content": f"Ты - архитектор решений" },
                        { "role": "user", "content": text_prompt },
                    ]
                ).choices[0].message.content
        open(solution_file_name, 'wt', encoding="UTF-8").write(text)

def gen(count):
    tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))
    for i, task in enumerate(tasks):
        if i < count:
            gen_text(task)

if __name__ == '__main__':
    gen(1)