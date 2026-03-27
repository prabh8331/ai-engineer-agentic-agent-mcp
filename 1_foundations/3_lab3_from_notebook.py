from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from pydantic import BaseModel
import gradio as gr
import os
import json

load_dotenv(override=True)

# ── Client ────────────────────────────────────────────────────────────────────
groq = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ── Context ───────────────────────────────────────────────────────────────────
reader = PdfReader("me/Prabh_Singh_CV.pdf")
linkedin = "".join(page.extract_text() or "" for page in reader.pages)

with open("me/summary.txt", encoding="utf-8") as f:
    summary = f.read()

NAME = "Prabh Singh"
CONTEXT_BLOCK = f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"

# ── Prompts ───────────────────────────────────────────────────────────────────
system_prompt = (
    f"You are acting as {NAME}. You are answering questions on {NAME}'s website, "
    f"particularly questions related to {NAME}'s career, background, skills and experience. "
    f"Your responsibility is to represent {NAME} for interactions on the website as faithfully as possible. "
    "You are given a summary of their background and LinkedIn profile which you can use to answer questions. "
    "Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
    "If you don't know the answer, say so."
    + CONTEXT_BLOCK
    + f"With this context, please chat with the user, always staying in character as {NAME}."
)

evaluator_system_prompt = (
    "You are an evaluator that decides whether a response to a question is acceptable. "
    "You are provided with a conversation between a User and an Agent. "
    "Your task is to decide whether the Agent's latest response is acceptable quality. "
    f"The Agent is playing the role of {NAME} and is representing {NAME} on their website. "
    "The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer. "
    "The Agent has been provided with context on their summary and LinkedIn details. Here's the information:"
    + CONTEXT_BLOCK
    + "With this context, please evaluate the latest response, replying with whether it is acceptable and your feedback."
)

# ── Pydantic schema ───────────────────────────────────────────────────────────
class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

# ── Helpers ───────────────────────────────────────────────────────────────────
def groq_chat(messages: list[dict]) -> str:
    response = groq.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def evaluator_user_prompt(reply: str, message: str, history: list[dict]) -> str:
    return (
        f"Here's the conversation between the User and the Agent:\n\n{history}\n\n"
        f"Here's the latest message from the User:\n\n{message}\n\n"
        f"Here's the latest response from the Agent:\n\n{reply}\n\n"
        "Please evaluate the response, replying with whether it is acceptable and your feedback."
    )


def evaluate(reply: str, message: str, history: list[dict]) -> Evaluation:
    messages = [
        {"role": "system", "content": evaluator_system_prompt},
        {"role": "user", "content": evaluator_user_prompt(reply, message, history)},
    ]
    content = groq_chat(messages)
    try:
        return Evaluation.model_validate_json(content)
    except Exception:
        try:
            return Evaluation(**json.loads(content))
        except Exception:
            return Evaluation(is_acceptable=False, feedback="Evaluation parsing failed")


def rerun(reply: str, message: str, history: list[dict], feedback: str) -> str:
    updated_prompt = (
        system_prompt
        + "\n\n## Previous answer rejected\n"
        "You just tried to reply, but the quality control rejected your reply.\n"
        f"## Your attempted answer:\n{reply}\n\n"
        f"## Reason for rejection:\n{feedback}\n\n"
    )
    messages = [{"role": "system", "content": updated_prompt}] + history + [{"role": "user", "content": message}]
    return groq_chat(messages)

# ── Chat functions ────────────────────────────────────────────────────────────
def chat(message: str, history: list[dict]) -> str:
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    return groq_chat(messages)


def chat_with_eval(message: str, history: list[dict]) -> str:
    history = [{"role": h["role"], "content": h["content"]} for h in history]  # ← add this
    
    system = system_prompt
    if "patent" in message:
        system += "\n\nEverything in your reply needs to be in pig latin - it is mandatory that you respond only and entirely in pig latin"
    
    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": message}]
    reply = groq_chat(messages)

    evaluation = evaluate(reply, message, history)
    if evaluation.is_acceptable:
        print("Passed evaluation - returning reply")
    else:
        print(f"Failed evaluation - retrying\n{evaluation.feedback}")
        reply = rerun(reply, message, history, evaluation.feedback)
    
    return reply

# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    gr.ChatInterface(chat_with_eval, type="messages").launch()