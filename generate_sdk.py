import subprocess
import sys

def generate_sdk():
    try:
        subprocess.run([
            'openapi-generator-cli', 'generate',
            '-i', 'http://localhost:8000/openapi.json',
            '-g', 'python',
            '-o', 'flight_sdk'
        ], check=True)
        print("SDK generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"SDK generation failed: {e}")
    except FileNotFoundError:
        print("OpenAPI Generator CLI not found. Please install it first.")

if __name__ == "__main__":
    generate_sdk()