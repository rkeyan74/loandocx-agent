from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr
from pagehit import get_page_hits
import os

load_dotenv(override=True)
MODEL_NAME = "gpt-5.4-mini"

#google_api_key = os.getenv("GOOGLE_API_KEY")
#GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
#gemini = OpenAI(api_key=google_api_key,base_url=GEMINI_BASE_URL)

openai = OpenAI()
system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content

if __name__ == "__main__":
    with gr.Blocks() as demo:

        gr.Image(
            "Loandocx_banner.jpg",
            show_label=False,
            container=False,
            height=180,
            elem_id="banner",
        )
        hit_counter = gr.Markdown(
            "Page Hits: 0",
            elem_id="hit-counter"
        )
        gr.ChatInterface(
            chat,
            examples=EXAMPLES,
            title="Agent LoanDocX",
            description="Talk to my AI Agent to explore LoanDocX",
            chatbot=gr.Chatbot(show_label=False),
        )
        demo.load(
           fn=get_page_hits,
           inputs=None,
           outputs=hit_counter,
        )
    demo.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )

