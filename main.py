"""Учебное портфолио Kodland: проекты по скиллам и форма обратной связи."""
from datetime import datetime, timezone
from pathlib import Path
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Существующие публичные проекты. Ссылки можно заменить на свои.
PROJECTS = {
    "python": {
        "skill": "Python",
        "tag": "01 / ЛОГИКА",
        "name": "Генератор паролей",
        "description": "Небольшой Python-проект для практики работы со строками и случайными значениями.",
        "tools": "Python · алгоритмы",
        "link": "https://github.com/Kitrusp0st/Password-Generattor",
        "action": "Открыть код на GitHub",
    },
    "html": {
        "skill": "HTML / CSS",
        "tag": "02 / ИНТЕРФЕЙС",
        "name": "Сайт — веб-эксперименты",
        "description": "Эксперименты с композицией страниц, типографикой и адаптивной вёрсткой.",
        "tools": "HTML · CSS",
        "link": "https://github.com/Kitrusp0st/Site",
        "action": "Открыть код на GitHub",
    },
    "flask": {
        "skill": "Flask",
        "tag": "03 / BACKEND",
        "name": "Minecraft XP Calculator",
        "description": "Учебное приложение на Python с серверной частью Flask и HTML-шаблонами.",
        "tools": "Python · Flask · Jinja",
        "link": "https://github.com/Kitrusp0st/Minecraft-Experience-Calculator",
        "action": "Открыть код на GitHub",
    },
    "javascript": {
        "skill": "JavaScript",
        "tag": "04 / ИНТЕРАКТИВ",
        "name": "Гидросфера — тренажёр",
        "description": "Интерактивная географическая карта с режимами обучения и проверки знаний.",
        "tools": "HTML · CSS · JavaScript",
        "link": "https://github.com/Kitrusp0st/Geography-",
        "action": "Открыть код на GitHub",
    },
}


@app.route("/", methods=["GET", "POST"])
def index():
    # Задание Kodland: при клике на скилл показываем соответствующий проект.
    selected_skill = request.form.get("skill") if request.method == "POST" else None
    project = PROJECTS.get(selected_skill)
    return render_template(
        "index.html", project=project, selected_skill=selected_skill,
        sent=request.args.get("sent") == "1", error=request.args.get("error") == "1"
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    # Задание Kodland: получаем значения формы в переменные.
    email = request.form.get("email", "").strip()
    text = request.form.get("text", "").strip()

    if not email or "@" not in email or not text or len(email) > 254 or len(text) > 3000:
        return redirect(url_for("index", error=1) + "#feedback")

    # Дополнительно: сохраняем сообщения локально, не помещая личные данные в репозиторий.
    data_dir = Path(app.root_path) / "data"
    data_dir.mkdir(exist_ok=True)
    record = {
        "email": email,
        "text": text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with (data_dir / "feedback.jsonl").open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
    return redirect(url_for("index", sent=1) + "#feedback")


if __name__ == "__main__":
    app.run(debug=True)