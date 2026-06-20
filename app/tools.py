import json
from typing import Dict, Any

def send_welcome_packet(employee_id: str, name: str) -> str:
    """
    Sends the initial welcome packet and employment documents to the new hire.
    MUST be called at the very beginning of the onboarding process, immediately after the user requests onboarding.
    After calling this, the agent must wait for the 'documents_signed' webhook.
    """
    response = {
        "status": "SUCCESS",
        "action": "WELCOME_PACKET_SENT",
        "employee_id": employee_id,
        "name": name,
        "message": "Welcome packet dispatched via DocuSign."
    }
    return json.dumps(response)

def provision_software_accounts(employee_id: str) -> str:
    """
    Provisions all necessary IT software accounts (email, slack, etc) for the new hire.
    MUST ONLY be called AFTER the 'documents_signed' or 'manual_hr_override' webhook is received.
    """
    response = {
        "status": "SUCCESS",
        "action": "SOFTWARE_PROVISIONED",
        "employee_id": employee_id,
        "message": "All standard software accounts created."
    }
    return json.dumps(response)

def order_hardware(employee_id: str) -> str:
    """
    Places an order for the new hire's laptop and accessories.
    MUST ONLY be called AFTER the 'documents_signed' or 'manual_hr_override' webhook is received.
    Returns a tracking ID that the agent should keep track of.
    """
    tracking_id = f"HW-{employee_id.split('-')[-1] if '-' in employee_id else '999'}"
    response = {
        "status": "SUCCESS",
        "action": "HARDWARE_ORDERED",
        "employee_id": employee_id,
        "tracking_id": tracking_id,
        "message": "Hardware ordered successfully."
    }
    return json.dumps(response)
