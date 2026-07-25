from datetime import datetime

def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text = f"[{now}] {message}"

    print(text)

    with open("logs.txt", "a", encoding="utf-8") as file:
        file.write(text + "\n")