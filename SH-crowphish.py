import os
import sys
import mimetypes
import json
import time
from google import genai
from google.genai import types
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# --- CONFIGURATION ---
ALIAS = "S.H. CROW"

# Initialize Rich Console
console = Console()

# --- 1. SECURE API KEY RETRIEVAL (GitHub Safe) ---
API_KEY = os.environ.get("GEMINI_API_KEY")

def print_banner():
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(f"[bold yellow]🛡️  {ALIAS} CYBER DEFENSE SYSTEMS 🛡️[/bold yellow]")
    grid.add_row("[dim]Phishing Triage & Intelligence Agent v1.0[/dim]")
    console.print(Panel(grid, style="bold yellow"))

# --- 2. PRE-FLIGHT CHECKS ---
print_banner()

if not API_KEY:
    console.print("[bold red]❌ CRITICAL ERROR: API Key missing.[/bold red]")
    console.print("\nTo fix this, run this command in your terminal:")
    console.print("[bold yellow]export GEMINI_API_KEY='your_actual_api_key_here'[/bold yellow]\n")
    sys.exit(1)

if len(sys.argv) < 2:
    console.print("[bold red]❌ Usage Error:[/bold red] You must provide an image path.")
    console.print("👉 [yellow]Correct Command:[/yellow] python3 SH-crowphish.py [italic]/path/to/image.jpg[/italic]")
    sys.exit(1)

IMAGE_PATH = sys.argv[1]

# --- 3. AUTO-DETECT IMAGE TYPE ---
mime_type, _ = mimetypes.guess_type(IMAGE_PATH)
if not mime_type:
    mime_type = "image/jpeg"

# --- 4. EXECUTION ---
client = genai.Client(api_key=API_KEY)

try:
    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()

    with Progress(
        SpinnerColumn("dots", style="bold yellow"),
        TextColumn("[bold yellow]Analyzing pixel data...[/bold yellow]"),
        transient=True
    ) as progress:
        task = progress.add_task("", total=None)
        time.sleep(1) 
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[
                types.Part.from_text(text="Analyze this email screenshot. Check the sender domain against the brand logo. Look for urgent language. Extract any visible URLs."),
                types.Part.from_bytes(
                    data=image_bytes, 
                    mime_type=mime_type
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.0,
                system_instruction="You are a Tier 3 SOC Analyst. Analyze the provided email screenshot for phishing indicators. Output your findings in strict JSON format.",
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "Final_Verdict": { "type": "string", "enum": ["Confirmed Phish", "Suspicious", "Safe"] },
                        "Phishing_Confidence_Score": { "type": "integer" },
                        "Key_Indicators": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "Indicator": { "type": "string" },
                                    "Severity": { "type": "string" }
                                }
                            }
                        },
                        "Explanation": { "type": "string" }
                    }
                }
            )
        )

    # --- 5. REPORT GENERATION ---
    data = json.loads(response.text)
    
    verdict = data.get("Final_Verdict", "Unknown")
    score = data.get("Phishing_Confidence_Score", 0)
    
    color = "green"
    if verdict == "Suspicious": color = "yellow"
    if verdict == "Confirmed Phish": color = "red"

    summary_text = Text()
    summary_text.append(f"VERDICT: {verdict}\n", style=f"bold {color}")
    summary_text.append(f"THREAT SCORE: {score}/100", style=f"bold {color}")
    
    console.print(Panel(summary_text, title="🔍 Analysis Results", border_style=color))

    table = Table(title="Observed Indicators", show_header=True, header_style="bold yellow")
    table.add_column("Severity", style="dim", width=12)
    table.add_column("Indicator", style="white")

    for item in data.get("Key_Indicators", []):
        sev = item.get("Severity", "Low")
        sev_color = "green"
        if sev == "Medium": sev_color = "yellow"
        if sev == "High" or sev == "Critical": sev_color = "red"
        
        table.add_row(f"[{sev_color}]{sev}[/{sev_color}]", item.get("Indicator", "N/A"))

    console.print(table)
    console.print(Panel(data.get("Explanation", "No details provided."), title="📝 Analyst Notes", border_style="blue"))

except FileNotFoundError:
    console.print(f"[bold red]❌ Error:[/bold red] Could not find file: [underline]{IMAGE_PATH}[/underline]")
except Exception as e:
    console.print(f"[bold red]❌ System Error:[/bold red] {e}")
