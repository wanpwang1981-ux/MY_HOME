import os
import argparse
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


def generate_image(api_key: str, image_path: str, prompt: str, output_path: str = "generated_image.png"):
    """
    Generates an image using a two-step process.

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

def main():
    """
    The main function that drives the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Generate an image using an input image and a prompt.")
    parser.add_argument("image_path", help="The path to the input image.")
    parser.add_argument("prompt", help="The text prompt for image generation.")
    parser.add_argument("output_path", help="The path to save the generated image.")
    parser.add_argument("--api_key", help="Your Google API key.", default=os.environ.get("API_KEY"))

    args = parser.parse_args()

    if not args.api_key:
        print("Error: API key not provided. Please set the API_KEY environment variable or use the --api_key argument.")
        return

    generate_image(
        api_key=args.api_key,
        image_path=args.image_path,
        prompt=args.prompt,
        output_path=args.output_path
    )

if __name__ == "__main__":
    main()
