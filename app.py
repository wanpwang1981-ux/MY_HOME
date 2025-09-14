import gradio as gr
import os
from image_creator import generate_image

# --- Helper Functions ---

def get_api_key():
    """
    Gets the Google API key from the environment.
    In a real app, you might want a more secure way to handle this.
    """
    return os.environ.get("API_KEY")

# --- Gradio Interface ---

def create_ui():
    """Creates and launches the Gradio UI."""

    # Check for API key
    if not get_api_key():
        print("ERROR: The 'API_KEY' environment variable is not set.")
        print("Please set it before running the application.")
        # You could also display this error in the UI itself
        # with gr.Error("API_KEY environment variable not set!").
        return

    with gr.Blocks(title="圖像創作者 (Image Creator)") as iface:
        gr.Markdown("# 圖像創作者 (Image Creator)")
        gr.Markdown("上傳一張圖片，輸入一段描述性文字，然後點擊「生成」來創造一張新的二創圖片。")

        with gr.Row():
            with gr.Column():
                input_image = gr.Image(type="filepath", label="輸入圖片 (Input Image)")
                prompt_text = gr.Textbox(label="提示文字 (Prompt)")
                generate_btn = gr.Button("生成 (Generate)")
            with gr.Column():
                output_image = gr.Image(label="生成結果 (Generated Image)")
                output_prompt = gr.Textbox(label="最終使用的提示 (Final Prompt)", interactive=False)

        def process_image(image_path, prompt):
            """Wrapper function to call the image generator and update UI."""
            if not image_path:
                raise gr.Error("請先上傳一張圖片 (Please upload an image first).")
            if not prompt:
                raise gr.Error("請輸入提示文字 (Please enter a prompt).")

            print("Starting image generation process...")
            # Define a unique output path for each generation
            output_filename = f"generated_{os.path.basename(image_path)}"
            output_filepath = os.path.join("output", output_filename)

            # Call the refactored generation function
            generated_img_path, final_prompt = generate_image(
                api_key=get_api_key(),
                image_path=image_path,
                prompt=prompt,
                output_path=output_filepath
            )

            if generated_img_path:
                return generated_img_path, final_prompt
            else:
                raise gr.Error("圖像生成失敗，請查看主控台錯誤訊息 (Image generation failed. Check the console for errors).")

        def clear_inputs():
            """Function to clear all inputs and outputs."""
            return None, "", None, ""

        clear_btn = gr.Button("清除 (Clear)")

        generate_btn.click(
            fn=process_image,
            inputs=[input_image, prompt_text],
            outputs=[output_image, output_prompt]
        )

        clear_btn.click(
            fn=clear_inputs,
            inputs=[],
            outputs=[input_image, prompt_text, output_image, output_prompt]
        )

    return iface

if __name__ == "__main__":
    app = create_ui()
    if app:
        app.launch()
