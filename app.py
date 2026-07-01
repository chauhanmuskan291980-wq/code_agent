import requests
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json"
}

history = []

def generate_response(prompt):
    # Add user message to history
    history.append(f"User: {prompt}")

    final_prompt = "\n".join(history) + "\nAssistant:"

    data = {
        "model": "code-assistant",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        actual_response = data["response"]

        # Add assistant response to history
        history.append(f"Assistant: {actual_response}")

        return actual_response
    else:
        return f"Error: {response.status_code}\n{response.text}"


interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your prompt"),
    outputs="text",
    title="Code Teaching Assistant",
    description="Ask coding questions to your local Ollama Code Assistant."
)

interface.launch()