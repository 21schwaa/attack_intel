# ReportFormAI.py
import os
from MemoryManager import MemoryManager
from Models import load_analysis_model

def load_report_template(template_path="report_template.txt"):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Report template file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_formatted_report_via_ai(template_path="report_template.txt"):
    memory = MemoryManager()
    memory.load_memory()
    recent_mem = memory.metadata[-10:] if len(memory.metadata) > 10 else memory.metadata

    memory_snippet = "\n\n".join([
        f"Command: {m['command']}\nSummary: {m['summary']}\nAnalysis: {m['analysis']}"
        for m in recent_mem
    ])

    report_template = load_report_template(template_path)

    prompt_template = f'''
You are a cybersecurity analyst completing a formal penetration testing report.

Here is the extracted information from a previous AI-guided reconnaissance session:

{memory_snippet}

Using this data, complete the following report format:

{report_template}
'''

    model = load_analysis_model()
    with model.chat_session():
        print("\n[+] Generating full-formatted report using AI...\n")
        report_text = model.generate(prompt_template, max_tokens=1000).strip()

    print("\n📄 Final Report Output:\n")
    print(report_text)
    return report_text

if __name__ == "__main__":
    path = input("Enter the report template filename (default: report_template.txt):\n>").strip()
    path = path if path else "report_template.txt"
    generate_formatted_report_via_ai(path)
