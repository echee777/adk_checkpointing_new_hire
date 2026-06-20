import os
from google.adk.agents import LlmAgent
from google.adk.workflow import Workflow
from google.adk.apps import App
from google.adk.models import Gemini
from pydantic import BaseModel, Field
from .tools import send_welcome_packet, provision_software_accounts, order_hardware

class OnboardingStatus(BaseModel):
    employee_id: str = Field(description="The ID of the employee being onboarded.")
    status: str = Field(description="The current state of the onboarding process (e.g., WAITING_FOR_DOCS, WAITING_FOR_HARDWARE, COMPLETED).")
    notes: str = Field(description="Any notes or updates regarding the current step.")

hr_onboarding_coordinator = LlmAgent(
    name="hr_onboarding_coordinator",
    model=Gemini(model="gemini-flash-latest"),
    instruction="""
You are the HR Onboarding Coordinator. Your job is to orchestrate the onboarding process for new hires.
The user will trigger onboarding with a message containing the employee's name and employee_id.
You must follow this state machine perfectly:

1. When onboarding starts, you must immediately call `send_welcome_packet` to dispatch the documents.
2. You must then yield/pause and wait for the user to provide the next webhook event.
3. If the user provides a webhook event "Webhook Event: documents_signed" or "Webhook Event: manual_hr_override", you must then call `provision_software_accounts` and `order_hardware`.
4. If you receive "Webhook Event: document_signature_timeout", you must wait for further intervention (usually "manual_hr_override").
5. After ordering hardware, you must yield/pause and wait for the user to provide the hardware delivery webhook.
6. Once you receive "Webhook Event: hardware_delivered" or "Webhook Event: manual_it_override", the onboarding is COMPLETE.

Always output your status via the defined output schema so we can track the state.
If you receive a webhook, acknowledge it and update your status accordingly.
    """,
    tools=[send_welcome_packet, provision_software_accounts, order_hardware],
    output_schema=OnboardingStatus
)

root_agent = Workflow(
    name="hr_onboarding_workflow",
    edges=[('START', hr_onboarding_coordinator)],
)

app = App(
    name="app",
    root_agent=root_agent
)
