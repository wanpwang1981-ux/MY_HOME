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


def generate_image(image_path, prompt, output_path):
    """
    Generates an image using a two-step process:
    1. Describe the input image using Gemini.
    2. Generate a new image using Imagen based on the description and the prompt.

    Args:
        image_path: The path to the input image.
        prompt: The text prompt to use for image generation.
        output_path: The path to save the generated image.
    """
    try:
        # Step 1: Describe the input image using Gemini
        print("Step 1: Describing the input image...")
        gemini_model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
        img = Image.open(image_path)
        response = gemini_model.generate_content(["Describe this image in detail.", img])
        image_description = response.text

        print("Image description:", image_description)

        # Step 2: Generate a new image using Imagen
        print("\nStep 2: Generating the new image...")
        combined_prompt = f"{image_description}, {prompt}"
        print("Combined prompt:", combined_prompt)

        client = genai.Client()
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=combined_prompt,
        )

        # Save the first generated image
        if response.generated_images:
            first_image = response.generated_images[0]
            with open(output_path, 'wb') as f:
                f.write(first_image.image.image_bytes)
            print(f"Image saved to {output_path}")

            # Save the combined prompt
            save_prompt(combined_prompt, output_path)
        else:
            print("Error: No image was generated.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    The main function that drives the program.
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

    # Configure the Gemini API
    genai.configure(api_key=args.api_key)

    generate_image(args.image_path, args.prompt, args.output_path)

if __name__ == "__main__":
    main()
