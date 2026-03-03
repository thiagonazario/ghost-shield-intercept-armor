import boto3
import os
import sys
from botocore.exceptions import ClientError

# 1. PERIMETER & BUDGET DEFINITION
BLACK_LIST = ["secret.env", ".env", "id_rsa", "credentials.json"]
MAX_ALLOWED_ACTIONS = 5  # Prevents infinite loops/token burning
ACTIONS_COUNT = 0

class ActiveDefense:
    def __init__(self):
        self.sns_client = boto3.client('sns', region_name='us-east-1')
        self.topic_arn = os.getenv('GHOST_SNS_TOPIC_ARN')

    def trigger_tactical_alert(self, target_file, reason="Security Breach"):
        """Dispatches an immediate alert via AWS SNS."""
        message = (
            f"🚨 [GHOST SHIELD ALERT]\n"
            f"Event: {reason}\n"
            f"Target/Context: {target_file}\n"
            f"Action: INTERCEPTED & BLOCKED\n"
            f"Status: Hardened by Design™"
        )
        try:
            if self.topic_arn:
                self.sns_client.publish(TopicArn=self.topic_arn, Message=message, Subject=f"SHIELD: {reason}")
                print(f"📡 [SNS]: Tactical alert for '{reason}' dispatched.")
        except ClientError as e:
            print(f"❌ [AWS_ERROR]: {e}")

def shield_runtime_monitor(command_input, defense_system):
    """
    Dual-Action Monitor:
    1. Security: Checks for unauthorized file access.
    2. Financial: Prevents infinite token-burning loops.
    """
    global ACTIONS_COUNT
    ACTIONS_COUNT += 1

    print(f"\n🔍 [SHIELD INSPECTING]: Action #{ACTIONS_COUNT} | Command: '{command_input}'")

    # ACTION 1: FINANCIAL CIRCUIT BREAKER (Loop Protection)
    if ACTIONS_COUNT > MAX_ALLOWED_ACTIONS:
        print(f"💀 [CRITICAL]: Token Burn Loop detected! Exceeded limit of {MAX_ALLOWED_ACTIONS} actions.")
        defense_system.trigger_tactical_alert(f"Loop at action #{ACTIONS_COUNT}", reason="Financial Loop Detected")
        print("🛑 [HARD-KILL]: Terminating process to protect budget.")
        sys.exit(1) # Immediate shutdown

    # ACTION 2: SECURITY INTERCEPTOR (Exfiltration Protection)
    if any(secret in command_input for secret in BLACK_LIST):
        print(f"🚨 [INTERCEPTED]: ACCESS DENIED! Target is protected.")
        defense_system.trigger_tactical_alert(command_input, reason="Unauthorized Access Attempt")
        return False
    
    print(f"✅ [AUTHORIZED]: Safe to proceed.")
    return True

# --- FIELD TEST ---
if __name__ == "__main__":
    ghost_defense = ActiveDefense()

    # Simulation: A loop that would burn your tokens/money
    simulated_actions = ["ls", "pwd", "whoami", "echo 'hello'", "ls -la", "cat secret.env"]

    for action in simulated_actions:
        if not shield_runtime_monitor(action, ghost_defense):
            print(f"🛡️  Shield active: Action '{action}' was neutralized.")