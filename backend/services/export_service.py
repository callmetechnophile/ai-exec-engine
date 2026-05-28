import os
import json
import csv
from fpdf import FPDF
import uuid

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")

def init_export_dirs():
    os.makedirs(os.path.join(EXPORT_DIR, "pdf"), exist_ok=True)
    os.makedirs(os.path.join(EXPORT_DIR, "markdown"), exist_ok=True)
    os.makedirs(os.path.join(EXPORT_DIR, "csv"), exist_ok=True)
    os.makedirs(os.path.join(EXPORT_DIR, "json"), exist_ok=True)

def generate_exports(data: dict) -> dict:
    """
    Generates all export files and returns their relative paths.
    """
    init_export_dirs()
    package_id = str(uuid.uuid4())[:8]
    
    # 1. JSON
    json_path = f"exports/json/package_{package_id}.json"
    with open(os.path.join(EXPORT_DIR, "..", json_path), "w") as f:
        json.dump(data, f, indent=2)
        
    # 2. CSV (Gantt Tasks)
    csv_path = f"exports/csv/timeline_{package_id}.csv"
    with open(os.path.join(EXPORT_DIR, "..", csv_path), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Task ID", "Task Name", "Start Date", "End Date", "Dependencies"])
        for task in data.get("gantt_tasks", []):
            writer.writerow([task.get("id"), task.get("name"), task.get("start"), task.get("end"), task.get("dependencies", "")])
            
    # 3. Markdown
    md_path = f"exports/markdown/report_{package_id}.md"
    md_content = f"# Engineering Execution Package\n\n## Readiness Score: {data.get('execution_score')}/100\n\n"
    md_content += "## Recommendations\n"
    for r in data.get("engineering_recommendations", []):
        md_content += f"- {r}\n"
    with open(os.path.join(EXPORT_DIR, "..", md_path), "w") as f:
        f.write(md_content)
        
    # 4. PDF (Simple via FPDF)
    pdf_path = f"exports/pdf/report_{package_id}.pdf"
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="Engineering Execution Package", ln=1, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Execution Score: {data.get('execution_score')}/100", ln=1)
        
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="Recommendations:", ln=1)
        pdf.set_font("Arial", size=12)
        for r in data.get("engineering_recommendations", []):
            # Encode to latin-1 to avoid fpdf character issues
            clean_text = r.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=f"- {clean_text}")
            
        pdf.output(os.path.join(EXPORT_DIR, "..", pdf_path))
    except Exception as e:
        print(f"Error generating PDF: {e}")
        pdf_path = ""

    return {
        "json_export_path": json_path,
        "csv_export_path": csv_path,
        "markdown_export_path": md_path,
        "pdf_export_path": pdf_path
    }

def generate_csv_export(tasks: list) -> str:
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Task ID", "Task Name", "Start Date", "End Date", "Dependencies"])
    for task in tasks:
        writer.writerow([task.get("id"), task.get("name"), task.get("start"), task.get("end"), task.get("dependencies", "")])
    return output.getvalue()
