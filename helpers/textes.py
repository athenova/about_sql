import os
import json
import glob

from openai import OpenAI

AI_TEXT_MODEL = 'chatgpt-4o-latest'

def gen_text(task, problem=True):
    folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    folder_name = glob.escape(f"{folder_name}/{task['name'].replace('/', ',')}")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    type = "description" if problem else "solution"
    text_file_name = f"{folder_name}/{type}.txt"

    client = OpenAI()
    if not os.path.exists(text_file_name):
        text_prompt = task[f"{type}_prompt"]
        text = client.chat.completions.create(
                    model=AI_TEXT_MODEL,
                    messages=[
                        { "role": "system", "content": f"Ты - архитектор решений" },
                        { "role": "user", "content": text_prompt },
                    ]
                ).choices[0].message.content
        open(text_file_name, 'wt', encoding="UTF-8").write(text)

def gen(count):
    tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))
    for i, task in enumerate(tasks):
        if i < count:
            gen_text(task, True)
            gen_text(task, False)

if __name__ == '__main__':
    gen(1)