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


# 🔥 STEP 6.1 — RULE-BASED IAM DETECTION (NEW)
def detect_iam_risks_rule_based(tf_code):
    risks = []

    # HIGH: Wildcard Action
    if '"Action": "*"' in tf_code or '"Action":"*"' in tf_code:
        risks.append({
            "type": "Wildcard Action",
            "severity": "HIGH",
            "description": "IAM policy allows all actions using '*'",
            "fix": "Restrict actions to only required services"
        })

    # HIGH: Wildcard Resource
    if '"Resource": "*"' in tf_code or '"Resource":"*"' in tf_code:
        risks.append({
            "type": "Wildcard Resource",
            "severity": "HIGH",
            "description": "IAM policy allows access to all resources",
            "fix": "Restrict resources to specific ARNs"
        })

    # MEDIUM: Service wildcard
    if "s3:*" in tf_code:
        risks.append({
            "type": "S3 Full Access",
            "severity": "MEDIUM",
            "description": "IAM policy allows full access to S3",
            "fix": "Limit S3 actions and specify bucket ARNs"
        })

    return risks


def analyze_with_ai(tf_code):
    tf_code = tf_code[:1500]

    prompt = f"""
You are an AWS IAM security expert.

Analyze ONLY IAM-related configurations in the Terraform code.
Ignore all non-IAM resources.

Identify security risks such as:
- Wildcard actions ("*")
- Wildcard resources ("*")
- Overly permissive IAM roles or policies
- Violations of least privilege principle

Classify each risk into severity levels:

- HIGH: If policy allows "*" in Action or Resource, or full administrative access
- MEDIUM: If permissions are overly broad (e.g., service-level wildcards like "s3:*")
- LOW: If minor issues like missing conditions or slightly excessive permissions

For each risk:
- Clearly explain why it is a security issue
- Provide a practical fix following least privilege principle

Return ONLY valid JSON in the following format:

{{
  "iam_risks": [
    {{
      "type": "",
      "severity": "",
      "description": "",
      "fix": ""
    }}
  ]
}}

Do not include any explanation outside JSON.
Do not add extra text.
Ensure output is valid JSON.

----------------------------------------
EXAMPLES:

Example 1:
Input:
{{ "Action": "*", "Resource": "*" }}

Output:
{{
  "iam_risks": [
    {{
      "type": "Wildcard Permissions",
      "severity": "HIGH",
      "description": "Policy allows all actions on all resources, which is a critical security risk.",
      "fix": "Restrict actions and resources to only what is required."
    }}
  ]
}}

Example 2:
Input:
{{ "Action": "s3:*", "Resource": "*" }}

Output:
{{
  "iam_risks": [
    {{
      "type": "Broad Service Permissions",
      "severity": "MEDIUM",
      "description": "Policy allows all S3 actions across all resources.",
      "fix": "Limit S3 actions and restrict resources to specific buckets."
    }}
  ]
}}

----------------------------------------

Terraform Code:
{tf_code}
"""

    print("Sending request to AI...\n")

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response['message']['content']

    print("\n🔍 Raw AI Output:\n")
    print(ai_output)

    # Clean markdown
    clean_output = ai_output.strip()

    if clean_output.startswith("```"):
        parts = clean_output.split("```")
        if len(parts) >= 2:
            clean_output = parts[1]
        if clean_output.startswith("json"):
            clean_output = clean_output[4:]
        clean_output = clean_output.strip()

    try:
        parsed_output = json.loads(clean_output)
    except json.JSONDecodeError:
        print("\n❌ ERROR: AI JSON invalid")
        return None

    if "iam_risks" not in parsed_output:
        print("\n⚠️ Missing iam_risks key")
        return None

    return parsed_output


def display_results(parsed_output):
    risks = parsed_output.get("iam_risks", [])

    print("\n🚨 IAM Security Risks Detected:\n")

    if not risks:
        print("✅ No IAM risks found")
        return

    for risk in risks:
        severity = risk.get("severity", "UNKNOWN")

        icon = "🔴" if severity == "HIGH" else "🟠" if severity == "MEDIUM" else "🟢"

        print(f"{icon} Severity: {severity}")
        print(f"Type: {risk.get('type')}")
        print(f"Description: {risk.get('description')}")
        print(f"Fix: {risk.get('fix')}")
        print("-" * 50)


if __name__ == "__main__":
    print("Reading Terraform files...\n")

    all_code = read_terraform_files()
    print(f"Code length: {len(all_code)} characters\n")

    # 🔥 STEP 6.2 — RULE-BASED CALL (NEW)
    rule_risks = detect_iam_risks_rule_based(all_code)

    analysis = analyze_with_ai(all_code)

    # 🔥 STEP 6.3 — MERGE RESULTS (NEW)
    if analysis:
        combined = {
            "iam_risks": rule_risks + analysis.get("iam_risks", [])
        }
        display_results(combined)
    else:
        display_results({"iam_risks": rule_risks})