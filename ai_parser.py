import os
import ollama
import json

TERRAFORM_DIR = "terraform"

def read_terraform_files():
    tf_code = ""

    for file in os.listdir(TERRAFORM_DIR):
        if file.endswith(".tf"):
            file_path = os.path.join(TERRAFORM_DIR, file)

            with open(file_path, "r") as f:
                content = f.read()
                tf_code += f"\n\n# File: {file}\n"
                tf_code += content

    return tf_code


def analyze_with_ai(tf_code):
    # Limit size for faster processing
    tf_code = tf_code[:1500]

    prompt = f"""
You are a cloud security expert.

Analyze the Terraform code and respond ONLY in JSON format.

Format:
{{
  "risks": ["risk1", "risk2"],
  "fixes": ["fix1", "fix2"]
}}

Rules:
- No explanation
- No extra text
- Only valid JSON

Terraform Code:
{tf_code}
"""

    print("Sending request to AI...\n")

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    ai_output = response['message']['content']

    # Try to parse JSON
    try:
        parsed = json.loads(ai_output)
        return parsed
    except json.JSONDecodeError:
        print("⚠️ AI did not return valid JSON. Raw output:\n")
        print(ai_output)
        return None


if __name__ == "__main__":
    print("Reading Terraform files...\n")

    all_code = read_terraform_files()

    print(f"Code length: {len(all_code)} characters\n")

    analysis = analyze_with_ai(all_code)

    if analysis:
        print("\n✅ Structured AI Output:\n")

        print("🔴 Risks:")
        for r in analysis["risks"]:
            print(f"- {r}")

        print("\n🟢 Fixes:")
        for f in analysis["fixes"]:
            print(f"- {f}")