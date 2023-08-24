import datetime
import json
import os
import re
import sys
from io import BufferedReader
from pathlib import Path
from typing import Tuple

import magic
import typer
from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

SCHEMA_FILE = "schema.json"
PROMPT_FILE = "prompt"

app = typer.Typer()


def pdf_to_text(file: BufferedReader) -> str:
    import pdftotext

    return "\n\n".join(pdftotext.PDF(file))


FILE_TYPE_HANDLERS = {"application/pdf": pdf_to_text}


def convert_to_text(filename: str | os.PathLike) -> str:
    filetype = magic.from_file(filename, mime=True)
    text_extractor = FILE_TYPE_HANDLERS.get(filetype)

    if not text_extractor:
        raise Exception(f"{filetype} not supported")

    with open(filename, "rb") as f:
        text = text_extractor(f)

    return text


def generate_prompt(resume: str) -> str:
    project_root = Path(__file__).parent.parent
    with open(project_root / SCHEMA_FILE, "r") as f:
        schema = f.read()
    with open(project_root / PROMPT_FILE, "r") as f:
        instruction = f.read()

    prompt = f"""### RESUME ###
{resume}
######

### JSONRESUME SCHEMA ###
{schema}
######

{instruction}

Current date : {datetime.datetime.now()}
    """

    return prompt


def ai_completion(prompt: str) -> str:
    result = None
    conversation_id = None
    access_token = os.environ.get("OPENAI_ACCESS_TOKEN")
    if not access_token:
        raise Exception("OPENAI_ACCESS_TOKEN not set")

    chatbot = Chatbot(config={"access_token": access_token})

    for data in chatbot.ask(prompt, auto_continue=True):
        result = str(data["message"])
        conversation_id = data["conversation_id"]

    if conversation_id is None:
        raise Exception("No conversation found")

    chatbot.delete_conversation(conversation_id)

    if result is None:
        raise Exception("No result found")

    return result


def extract(impure_text: str) -> Tuple[str, str]:
    pattern = r"```json(.*?)```(.*?)$"
    match = re.search(pattern, impure_text, re.DOTALL)
    if not match:
        raise Exception("No json codeblock found")

    json_data = json.loads(match.group(1).strip())
    if "$schema" in json_data:
        del json_data["$schema"]

    summary = match.group(2).strip()

    return (json_data, summary)


@app.command()
def main(resume_file: str):
    load_dotenv()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=Console(file=sys.stderr),
    ) as progress:
        task = progress.add_task(description="Converting to jsonresume...")
        json_resume, _ = extract(
            ai_completion(generate_prompt(convert_to_text(resume_file)))
        )
        progress.update(task, completed=1)
        progress.print("✨ [green]Successfully converted to jsonresume")

    print(json.dumps(json_resume, indent=2))
