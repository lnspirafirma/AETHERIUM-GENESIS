import sys
import os
import subprocess
import uuid
import hashlib
from datetime import datetime, timezone

# [SYSTEM SETUP] Add project root to path to import Core modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# [CORE INTEGRATION] Import philosophy and identity modules
try:
    from core.signature import OriginMetadata, AISource
    from core.envelope import AetherIntent
except ImportError as e:
    print(f"❌ Critical Error: Unable to link with AETHERIUM Core. {e}")
    print("Please run this script from the project root directory.")
    sys.exit(1)

class CommitmentRitual:
    def __init__(self):
        self.architect_identity = AISource.HUMAN_ARCHITECT
        self.session_id = str(uuid.uuid4())[:8]

    def _check_git_status(self) -> list[str]:
        """Verifies the repository state and retrieves staged files."""
        try:
            # Check if inside git tree
            subprocess.run(
                ['git', 'rev-parse', '--is-inside-work-tree'],
                check=True, capture_output=True
            )
            # Get staged files
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                check=True, capture_output=True, text=True, encoding='utf-8'
            )
            files = [f for f in result.stdout.strip().split('\n') if f]
            return files
        except subprocess.CalledProcessError:
            print("❌ Error: Not a valid Git repository or Git is not installed.")
            sys.exit(1)

    def _get_architect_intent(self) -> tuple[str, str]:
        """Interactively asks the Architect for their Intent."""
        print("\n--- 🏛️  AETHERIUM COMMIT RITUAL ---")
        print(f"Architect: {self.architect_identity.value}")
        print(f"Session:   {self.session_id}")
        print("-----------------------------------")
        
        # 1. Select Intent Category (Mapping to AetherIntent roughly)
        print("Select your Intent Category:")
        print(" [1] UPDATE_LOGIC  (Refactoring, Logic change)")
        print(" [2] ASSERT_FACT   (Documentation, Config, Truth)")
        print(" [3] NEW_FEATURE   (Adding new capabilities)")
        print(" [4] HOTFIX        (Emergency repair)")
        
        choice = input("\nSelect [1-4]: ").strip()
        category_map = {
            "1": "UPDATE_LOGIC",
            "2": "ASSERT_FACT",
            "3": "NEW_FEATURE",
            "4": "HOTFIX"
        }
        category = category_map.get(choice, "GENERAL_UPDATE")

        # 2. The Message
        print(f"\n[{category}] Please state your intention clearly:")
        message = input(">>> ").strip()
        
        if not message:
            print("\n❌ Void Intent detected. Commitment aborted.")
            sys.exit(1)
            
        return category, message

    def _seal_the_envelope(self, category: str, message: str) -> str:
        """
        Constructs the final commit message, embedding metadata 
        like an Aether Envelope.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Generate a simple integrity hash (Proof of Thought)
        content_to_hash = f"{self.architect_identity.value}:{message}:{timestamp}"
        integrity_hash = hashlib.sha256(content_to_hash.encode()).hexdigest()[:16]

        # Construct the formatted Git Message
        # Format:
        # <CATEGORY>: <Short Message>
        # 
        # [AETHERIUM-METADATA]
        # Source: Human-Creator
        # Trace-ID: <UUID>
        # Integrity: <Hash>
        
        final_log = (
            f"{category}: {message}\n\n"
            f"[AETHERIUM-METADATA]\n"
            f"Source: {self.architect_identity.value}\n"
            f"Timestamp: {timestamp}\n"
            f"Session-ID: {self.session_id}\n"
            f"Integrity-Hash: {integrity_hash}"
        )
        return final_log

    def perform(self):
        """Executes the ritual."""
        staged_files = self._check_git_status()
        
        if not staged_files:
            print("⚠️  Status: No changes staged (The Altar is empty).")
            print("   Please use 'git add <file>' first.")
            sys.exit(0)

        print(f"Found {len(staged_files)} artifact(s) ready for commitment.")
        
        # Get Input
        category, message = self._get_architect_intent()
        
        # Seal the Message
        final_commit_msg = self._seal_the_envelope(category, message)
        
        # Execute Git Commit securely
        print("\n⚡ Sealing the intent into Devordota (Git History)...")
        try:
            subprocess.run(
                ['git', 'commit', '-F', '-'],
                input=final_commit_msg,
                check=True, capture_output=True, text=True, encoding='utf-8'
            )
            print("\n✅ Ritual Complete. The intent has been recorded.")
            
            # Show the log verification
            subprocess.run(['git', 'log', '-1', '--stat'], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Ritual Failed: {e.stderr}")

if __name__ == "__main__":
    ritual = CommitmentRitual()
    ritual.perform()
