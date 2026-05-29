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
    
    # Extract data safely
    score = data.get('execution_score', 0)
    components = data.get("optimized_components", []) or data.get("engineering_components", [])
    papers = data.get("research_papers", [])
    gantt = data.get("gantt_tasks", [])
    
    # 1. JSON
    json_path = f"exports/json/package_{package_id}.json"
    with open(os.path.join(EXPORT_DIR, "..", json_path), "w") as f:
        json.dump(data, f, indent=2)
        
    # 2. CSV (Gantt Tasks)
    csv_path = f"exports/csv/timeline_{package_id}.csv"
    with open(os.path.join(EXPORT_DIR, "..", csv_path), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Task ID", "Task Name", "Start Date", "End Date", "Dependencies"])
        for task in gantt:
            writer.writerow([task.get("id"), task.get("name"), task.get("start"), task.get("end"), task.get("dependencies", "")])
            
    # 3. Markdown
    md_path = f"exports/markdown/report_{package_id}.md"
    md_content = f"# Engineering Execution Package\n\n## Readiness Score: {score}/100\n\n"
    
    md_content += "## Bill of Materials\n| COMPONENT NAME | COMPONENT TYPE | PURPOSE |\n| --- | --- | --- |\n"
    for c in components:
        md_content += f"| {c.get('name', 'N/A')} | Hardware | {c.get('description', 'N/A')} |\n"
        
    md_content += "\n## Research Papers\n"
    for i, p in enumerate(papers, 1):
        md_content += f"[{i}] {p.get('title', 'Unknown')}, [Online]. Available: {p.get('url', '#')}\n"
        
    md_content += "\n## Feasibility & Recommendations\n"
    for r in data.get("engineering_recommendations", []):
        md_content += f"- {r}\n"
        
    md_content += "\n## Gantt Chart Timeline\n"
    for task in gantt:
        md_content += f"- {task.get('name')} ({task.get('start')} to {task.get('end')})\n"
        
    with open(os.path.join(EXPORT_DIR, "..", md_path), "w") as f:
        f.write(md_content)
        
    # 4. PDF (Simple via FPDF)
    pdf_path = f"exports/pdf/report_{package_id}.pdf"
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add Page Border
        pdf.rect(5.0, 5.0, 200.0, 287.0)
        
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="Engineering Execution Package", ln=1, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Execution Score: {score}/100", ln=1)
        pdf.ln(5)
        
        # Components Table
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="Bill of Materials", ln=1)
        pdf.set_font("Arial", size=10, style="B")
        pdf.cell(60, 10, txt="COMPONENT NAME", border=1)
        pdf.cell(30, 10, txt="TYPE", border=1)
        pdf.cell(100, 10, txt="PURPOSE", border=1, ln=1)
        pdf.set_font("Arial", size=8)
        for c in components:
            name = str(c.get('name', 'N/A'))[:30].encode('latin-1', 'replace').decode('latin-1')
            desc = str(c.get('description', 'N/A'))[:70].encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(60, 10, txt=name, border=1)
            pdf.cell(30, 10, txt="Hardware", border=1)
            pdf.cell(100, 10, txt=desc, border=1, ln=1)
        pdf.ln(5)
        
        # Research Papers Table
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="Research Papers", ln=1)
        pdf.set_font("Arial", size=10, style="B")
        pdf.cell(60, 10, txt="PAPER NAME", border=1)
        pdf.cell(90, 10, txt="MAIN PURPOSE", border=1)
        pdf.cell(40, 10, txt="LINK", border=1, ln=1)
        pdf.set_font("Arial", size=8)
        for p in papers:
            title = str(p.get('title', 'Unknown'))[:35].encode('latin-1', 'replace').decode('latin-1')
            purpose = str(p.get('summary', 'Research snippet'))[:65].encode('latin-1', 'replace').decode('latin-1')
            url = str(p.get('url', '#'))
            pdf.cell(60, 10, txt=title, border=1)
            pdf.cell(90, 10, txt=purpose, border=1)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(40, 10, txt="[Read Paper]", border=1, ln=1, link=url)
            pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        # Recommendations
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="Feasibility & Recommendations", ln=1)
        pdf.set_font("Arial", size=11)
        for r in data.get("engineering_recommendations", []):
            clean_text = str(r).encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 8, txt=f"{chr(149)}  {clean_text}")
        pdf.ln(5)
        
        # Gantt Timeline Table
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="Gantt Chart Timeline", ln=1)
        pdf.set_font("Arial", size=10, style="B")
        pdf.cell(40, 10, txt="PHASE", border=1)
        pdf.cell(90, 10, txt="WORK", border=1)
        pdf.cell(60, 10, txt="TIME REQUIRED", border=1, ln=1)
        pdf.set_font("Arial", size=8)
        for task in gantt:
            t_name = str(task.get('name', '')).encode('latin-1', 'replace').decode('latin-1')
            phase = t_name.split(':')[0][:25] if ':' in t_name else "Execution"
            work = t_name[:60]
            time_req = f"{task.get('start')} to {task.get('end')}"
            pdf.cell(40, 10, txt=phase, border=1)
            pdf.cell(90, 10, txt=work, border=1)
            pdf.cell(60, 10, txt=time_req, border=1, ln=1)
            
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
