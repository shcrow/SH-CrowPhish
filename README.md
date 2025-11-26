# 🛡️ SH-CrowPhish: AI-Powered Phishing Triage Tool

**Developed by S.H. Crow**

An automated cybersecurity tool that leverages the **Gemini 2.5 Flash** multimodal model to analyze suspicious emails. It performs OCR, brand logo matching, and linguistic threat analysis to assign a "Phishing Confidence Score" to any screenshot.

## 🚀 Features
* **AI Vision Analysis:** Detects mismatched sender domains and fake logos.
* **Automated Scoring:** Assigns a 0-100 threat score based on IOCs.
* **Universal Support:** Works with JPG, PNG, and WebP formats.
* **JSON Output:** Produces structured logs ready for SOAR integration.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/SH-CrowPhish.git](https://github.com/YOUR_USERNAME/SH-CrowPhish.git)
    cd SH-CrowPhish
    ```

2.  **Install dependencies:**
    ```bash
    pip3 install google-genai rich
    ```

3.  **Set your API Key:**
    ```bash
    export GEMINI_API_KEY='your_google_api_key_here'
    ```

## 💻 Usage

Run the tool against any email screenshot:

```bash
python3 SH-crowphish.py /path/to/suspicious_email.png
