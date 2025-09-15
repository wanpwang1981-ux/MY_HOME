import os
import google.generativeai as genai
from PIL import Image

# A dictionary to store the generated images and their prompts
image_data = {}

def save_prompt(prompt, output_path):
    """
    Saves the prompt to a text file.

    Args:
        prompt: The text prompt to save.
        output_path: The path to the output image.
    """
    prompt_path = os.path.splitext(output_path)[0] + ".txt"
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    print(f"Prompt saved to {prompt_path}")


import base64

def generate_text_to_image(api_key: str, prompt: str, output_path: str = "generated_image.png"):
    """
    Generates an image from a text prompt using the Gemini 2.5 Flash model.

    Args:
        api_key: Your Google API key.
        prompt: The text prompt to use for image generation.
        output_path: The path to save the generated image.

    Returns:
        The path to the generated image (str), or None if an error occurs.
    """
    try:
        genai.configure(api_key=api_key)
        print("Generating image from text using Gemini 2.5 Flash...")

        model = genai.GenerativeModel('gemini-2.5-flash-image-preview')

        # Correct generation config, as hinted by the user's original JS code
        generation_config = {
            "response_modalities": ["IMAGE", "TEXT"],
        }

        response = model.generate_content([prompt], generation_config=generation_config)

        if response.candidates and response.candidates[0].content.parts:
            # Find the part that contains the image data
            image_part = None
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_part = part
                    break

            if image_part and image_part.inline_data.data:
                base64_data = image_part.inline_data.data
                image_data = base64.b64decode(base64_data)

                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                with open(output_path, 'wb') as f:
                    f.write(image_data)
                print(f"Image saved to {output_path}")

                save_prompt(prompt, output_path)
                return output_path
            else:
                print("Error: No inline image data found in the API response.")
                print(f"Full response: {response}")
                return None
        else:
            print("Error: Invalid response structure from API.")
            print(f"Full response: {response}")
            return None

    except Exception as e:
        print(f"An error occurred in generate_text_to_image: {e}")
        return None

def generate_text_and_image_to_image(api_key: str, image_path: str, prompt: str, output_path: str = "generated_image.png"):
    """
    Generates an image using a two-step process (text+image to image).

    Args:
        api_key: Your Google API key.
        image_path: The path to the input image.
        prompt: The text prompt to use for image generation.
        output_path: The path to save the generated image.

    Returns:
        A tuple containing:
        - The path to the generated image (str).
        - The combined prompt used for generation (str).
        Returns (None, None) if an error occurs.
    """
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)

        # Step 1: Describe the input image using Gemini
        print("Step 1: Describing the input image...")
        gemini_model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
        img = Image.open(image_path)
        response = gemini_model.generate_content(["Describe this image in detail.", img])
        image_description = response.text
        print(f"Image description: {image_description}")

        # Step 2: Generate a new image using Imagen
        print("\nStep 2: Generating the new image...")
        combined_prompt = f"{image_description}, {prompt}"
        print(f"Combined prompt: {combined_prompt}")

        client = genai.Client()
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=combined_prompt,
        )

        if response.generated_images:
            first_image = response.generated_images[0]
            # Ensure the output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'wb') as f:
                f.write(first_image.image.image_bytes)
            print(f"Image saved to {output_path}")

            save_prompt(combined_prompt, output_path)
            return output_path, combined_prompt
        else:
            print("Error: No image was generated.")
            return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# The main block is removed as this script is now intended to be used as a library.
