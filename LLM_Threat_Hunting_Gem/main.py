import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class ThreatHuntingGem:
    def __init__(self):
        # Initialize the GenAI client
        self.client = genai.Client(api_key=API_KEY)
        self.model_id = 'gemini-2.5-pro'
        
        # Load the system prompt that defines the CIRT/CTH Persona and strict rules
        self.system_instruction = self._load_system_prompt("system_prompt.txt")
        
        # Upload context schemas and templates to the Gemini File API
        self.context_files = self._upload_context_files()
        
        # Configure the model parameters
        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.1,  # Low temperature to prevent syntax hallucination
            top_p=0.95,
        )
        
        # Start a persistent chat session
        self.chat_session = self.client.chats.create(
            model=self.model_id,
            config=self.config
        )

    def _load_system_prompt(self, filepath: str) -> str:
        """Loads the strict Persona and ruleset from a local text file."""
        with open(filepath, 'r') as file:
            return file.read()

    def _upload_context_files(self) -> list:
        """
        Uploads massive schema PDFs and report templates to the Gemini File API.
        This provides perfect data dictionary context without massive token bloat.
        """
        print("[*] Uploading schema guides and report templates to the Gem...")
        files_to_upload = [
            "context_files/XDR_Schema_Guide.pdf",
            "context_files/SIEM_Field_Guide.pdf",
            "context_files/SIEM_Usage_guide.pdf",
            "context_files/IR_Hunt_Report_Template.docx"
        ]
        
        uploaded_files = []
        for file_path in files_to_upload:
            # Note: In a live environment, ensure these files exist in the directory
            try:
                uploaded_file = self.client.files.upload(file=file_path)
                uploaded_files.append(uploaded_file)
                print(f"    -> Uploaded: {uploaded_file.display_name}")
            except FileNotFoundError:
                print(f"    -> [SKIPPED] File not found for portfolio demonstration: {file_path}")
            
        # Wait briefly for files to be processed by the API
        time.sleep(5)
        return uploaded_files

    def initialize_session(self):
        """Triggers the required startup sequence dictated by the system prompt."""
        print("\n--- Initializing Session ---")
        response = self.chat_session.send_message("Initiate Session Startup.")
        print(f"\nGem: {response.text}")

    def ingest_cti_and_hunt(self, user_name: str, cti_payload: str):
        """
        Phase 1: Submits the analyst's name and the raw CTI (text or URL).
        The Gem will return a formatted IR Hunt Report based on the injected schemas.
        """
        print("\n[*] Processing CTI and generating Hunt Report...")
        
        # We pass the uploaded schema files alongside the user's prompt
        prompt_contents = [
            *self.context_files,
            f"My name is {user_name}. Here is the CTI to analyze: {cti_payload}"
        ]
        
        response = self.chat_session.send_message(prompt_contents)
        print("\n--- Hunt Report Generated ---\n")
        print(response.text)

    def analyze_results(self, query_results: str):
        """
        Phase 2: Submits SIEM/XDR query output back to the Gem for analysis 
        against the previously generated TTP profile.
        """
        print("\n[*] Analyzing raw query results...")
        prompt = f"Analyze these results:\n\n{query_results}"
        response = self.chat_session.send_message(prompt)
        print("\n--- Analysis & Clarification ---\n")
        print(response.text)

    def finalize_report(self):
        """Phase 3: Triggers the final conclusion and executive summary."""
        print("\n[*] Finalizing executive summary...")
        response = self.chat_session.send_message("Generate final conclusion.")
        print("\n--- Final Conclusion ---\n")
        print(response.text)

if __name__ == "__main__":
    # Example Execution Flow
    gem = ThreatHuntingGem()
    
    # Trigger the Gem's mandated startup message
    gem.initialize_session()
    
    # Simulate a user providing CTI
    analyst_name = "Jane Doe"
    raw_cti = "Threat actors are exploiting CVE-2024-XXXX, dropping a payload named 'svchost.exe' in C:\\Users\\Public\\ and communicating with C2 domain evil-actor[.]com over port 443."
    
    # Run Phase 1
    gem.ingest_cti_and_hunt(user_name=analyst_name, cti_payload=raw_cti)
    
    # Simulate Phase 2 (Providing SIEM hits)
    mock_siem_results = "Hit found: hostname=host-01, process=svchost.exe, path=C:\\Users\\Public\\, network_dest=evil-actor[.]com"
    gem.analyze_results(mock_siem_results)
    
    # Run Phase 3
    gem.finalize_report()