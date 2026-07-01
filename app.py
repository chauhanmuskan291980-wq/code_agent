import os
import gradio as gr
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="codellama/CodeLlama-7b-Instruct-hf",
    token=HF_TOKEN
)

history = []

def generate_response(prompt):
    history.append(f"User: {prompt}")

    final_prompt = "\n".join(history) + "\nAssistant:"

    try:
        response = client.text_generation(
            final_prompt,
            max_new_tokens=300,
            temperature=0.7,
            return_full_text=False
        )

        history.append(f"Assistant: {response}")
        return response

    except Exception as e:
        return f"Error: {str(e)}"


interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(
        lines=4,
        placeholder="Ask any coding question..."
    ),
    outputs="text",
    title="Code Assistant by Muskan Chauhan",
    description="A coding assistant built using Python, Gradio, and Hugging Face."
)

interface.launch()