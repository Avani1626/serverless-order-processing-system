from iam_analyzer import analyze_iam
from cost_analyzer import analyze_cost


def run_analysis():
    iam_risks = analyze_iam()
    cost_risks = analyze_cost()

    return {
        "iam_risks": iam_risks,
        "cost_risks": cost_risks
    }


if __name__ == "__main__":
    data = run_analysis()
    print(data)