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


# 🔥 IAM RULE-BASED DETECTION
def detect_iam_risks_rule_based(tf_code):
    risks = []

    if '"Action": "*"' in tf_code or '"Action":"*"' in tf_code:
        risks.append({
            "type": "Wildcard Action",
            "severity": "HIGH",
            "description": "IAM policy allows all actions using '*'",
            "fix": "Restrict actions to only required services"
        })

    if '"Resource": "*"' in tf_code or '"Resource":"*"' in tf_code:
        risks.append({
            "type": "Wildcard Resource",
            "severity": "HIGH",
            "description": "IAM policy allows access to all resources",
            "fix": "Restrict resources to specific ARNs"
        })

    if "s3:*" in tf_code:
        risks.append({
            "type": "S3 Full Access",
            "severity": "MEDIUM",
            "description": "IAM policy allows full access to S3",
            "fix": "Limit S3 actions and specify bucket ARNs"
        })

    return risks


# 💸 COST RULE-BASED DETECTION
def detect_cost_risks(tf_code):
    risks = []

    if "aws_nat_gateway" in tf_code:
        risks.append({
            "type": "NAT Gateway Cost",
            "severity": "HIGH",
            "description": "NAT Gateway has high hourly and data processing costs",
            "fix": "Use VPC endpoints or NAT instance to reduce cost"
        })

    if "t3.large" in tf_code or "t3.xlarge" in tf_code:
        risks.append({
            "type": "Expensive EC2 Instance",
            "severity": "MEDIUM",
            "description": "Using large EC2 instances increases cost",
            "fix": "Use smaller instance types or auto-scaling"
        })

    return risks


# 🤖 AI IAM ANALYSIS
def analyze_with_ai(tf_code):
    tf_code = tf_code[:1500]

    prompt = f"""
You are an AWS IAM security expert.

Analyze ONLY IAM-related configurations in the Terraform code.

Return ONLY JSON:

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

Terraform Code:
{tf_code}
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response['message']['content']

    clean_output = ai_output.strip().replace("```json", "").replace("```", "")

    try:
        parsed_output = json.loads(clean_output)
        return parsed_output
    except:
        print("❌ AI JSON parsing failed")
        return None
    
    # 💸 AI COST ANALYSIS
def analyze_cost_with_ai(tf_code):
    tf_code = tf_code[:1500]

    prompt = f"""
You are an AWS cost optimization expert.

Analyze ONLY cost-related issues in the Terraform code.

Focus on:
- Expensive resources
- Over-provisioning
- Inefficient configurations

Classify severity:
- HIGH: Very expensive resources (e.g., NAT Gateway)
- MEDIUM: Over-provisioned resources
- LOW: Minor inefficiencies

Return ONLY valid JSON:

{{
  "cost_risks": [
    {{
      "type": "",
      "severity": "",
      "description": "",
      "fix": ""
    }}
  ]
}}

----------------------------------------

Example:

Input:
resource "aws_nat_gateway" "main" {{}}

Output:
{{
  "cost_risks": [
    {{
      "type": "NAT Gateway Cost",
      "severity": "HIGH",
      "description": "NAT Gateway incurs high hourly and data processing costs",
      "fix": "Use VPC endpoints or NAT instance"
    }}
  ]
}}

----------------------------------------

Terraform Code:
{tf_code}
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response['message']['content']

    clean_output = ai_output.strip().replace("```json", "").replace("```", "")

    try:
        parsed_output = json.loads(clean_output)
        return parsed_output
    except:
        print("❌ Cost AI JSON parsing failed")
        return None


# 🖥 DISPLAY IAM RESULTS
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


# 💸 DISPLAY COST RESULTS
def display_cost_results(cost_risks):
    print("\n💸 Cost Risks Detected:\n")

    if not cost_risks:
        print("✅ No cost risks found")
        return

    for risk in cost_risks:
        severity = risk.get("severity", "UNKNOWN")
        icon = "🔴" if severity == "HIGH" else "🟠" if severity == "MEDIUM" else "🟢"

        print(f"{icon} Severity: {severity}")
        print(f"Type: {risk.get('type')}")
        print(f"Description: {risk.get('description')}")
        print(f"Fix: {risk.get('fix')}")
        print("-" * 50)


# 🚀 MAIN EXECUTION
if __name__ == "__main__":
    print("Reading Terraform files...\n")

    all_code = read_terraform_files()
    print(f"Code length: {len(all_code)} characters\n")

    # 🔐 IAM RULES
    iam_rule_risks = detect_iam_risks_rule_based(all_code)

    # 💸 COST RULES
    cost_risks = detect_cost_risks(all_code)

    ai_cost_analysis = analyze_cost_with_ai(all_code)

    # 🤖 AI IAM
    ai_analysis = analyze_with_ai(all_code)

    # 🔥 MERGE IAM
    if ai_analysis:
        combined_iam = {
            "iam_risks": iam_rule_risks + ai_analysis.get("iam_risks", [])
        }
    else:
        combined_iam = {
            "iam_risks": iam_rule_risks
        }
    # 🔥 MERGE COST RESULTS
    if ai_cost_analysis:
        combined_cost = cost_risks + ai_cost_analysis.get("cost_risks", [])
    else:
        combined_cost = cost_risks
     
    # 🖥 FINAL OUTPUT
    display_results(combined_iam)
    display_cost_results(cost_risks)