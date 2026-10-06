import json
import os
from jira_service import create_jira_ticket
from email_service import send_escalation_email

def process_ticket_pipeline(category, query_text):
    """
    Simulates the RAG Retrieval and Validation/Confidence engine for ShopAssist AI,
    including automated Jira and Email escalation for low-confidence queries.
    """
    # 1. Path to your knowledge.json file
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge.json")
    
    # Default fallback policies if JSON doesn't load
    policies = {
        "Returns & Refunds": "Eligible products can be returned within 30 days of delivery with original tags.",
        "Order Delivery": "Standard shipping takes 3-5 business days. Tracking updates are sent via email.",
        "Payment Dispute": "Refunds for failed transactions are automatically processed back to the original payment method within 5-7 business days.",
        "Damaged Item": "Items damaged upon arrival qualify for an immediate replacement or full refund upon photo verification."
    }
    
    # 2. Try loading knowledge from knowledge.json (Person 2's module)
    try:
        if os.path.exists(kb_path):
            with open(kb_path, "r") as f:
                kb_data = json.load(f)
                matched_policy = kb_data.get(category, policies.get(category, "Standard support policy applies."))
        else:
            matched_policy = policies.get(category, "Standard support policy applies.")
    except Exception as e:
        matched_policy = "Error loading knowledge base: " + str(e)

    # 3. Validation & Confidence Engine (Person 3's module)
    base_confidence = 85.0
    if len(query_text.strip()) > 15:
        base_confidence = 96.4
    elif len(query_text.strip()) < 5:
        base_confidence = 52.0  # Low confidence if query is too vague
        
    # Decision threshold: >= 70% is Automated Resolution, else Escalation
    if base_confidence >= 70.0:
        outcome = "Automated Resolution"
        resolution_text = f"Based on store policy ({category}), your request is approved. {matched_policy}"
    else:
        outcome = "Escalated"
        resolution_text = "Query requires manual agent verification due to insufficient detail or policy exception."
        
        # 4. Trigger Person 4's Enterprise Integrations on escalation
        create_jira_ticket(
            summary=f"Escalated Support Ticket: {category}",
            description=f"Query: {query_text}\nConfidence: {base_confidence}%",
            priority="High"
        )
        send_escalation_email(
            recipient_email="ops-lead@shopassist.ai",
            subject=f"Action Required: Escalated Support Ticket ({category})",
            body=f"A support ticket has been flagged for manual review.\n\nQuery: {query_text}\nConfidence Score: {base_confidence}%"
        )

    return {
        "matched_policy": matched_policy,
        "confidence": f"{base_confidence}%",
        "outcome": outcome,
        "resolution": resolution_text
    }