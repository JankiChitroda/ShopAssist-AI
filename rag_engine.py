import json
import os
from jira_service import create_jira_ticket
from email_service import send_escalation_email

def process_ticket_pipeline(category, query_text, customer_email="", order_ref=""):
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
        
    jira_key = None
    real_order_ref = order_ref.strip() if order_ref else "#ORD-7741"
    real_customer_email = customer_email.strip() if customer_email else os.getenv("SMTP_EMAIL", "yashwanthaagunuri15@gmail.com")

    from datetime import datetime
    created_at_str = datetime.now().strftime("%b %d, %Y, %I:%M %p")
    from email_service import extract_customer_name, send_auto_resolved_email

    ticket_id = None

    # Decision threshold: >= 70% is Automated Resolution, else Escalation
    if base_confidence >= 70.0:
        outcome = "Automated Resolution"
        resolution_text = f"Based on store policy ({category}), your request is approved. {matched_policy}"
        ticket_id = f"SHOP-AUTO-{real_order_ref.replace('#', '').replace('ORD-', '')}"
        
        ticket_details = {
            "ticket_id": ticket_id,
            "jira_key": ticket_id,
            "category": category,
            "priority": "Normal",
            "status": "Approved",
            "order_ref": real_order_ref,
            "customer_email": real_customer_email,
            "customer_name": extract_customer_name(real_customer_email, "Yashwanth"),
            "created_at": created_at_str,
            "query_text": query_text,
            "resolution": resolution_text,
            "resolution_draft": resolution_text,
            "confidence": f"{base_confidence}%"
        }

        # Send side-by-side HTML email for auto-resolved ticket
        send_auto_resolved_email(
            recipient_email=real_customer_email,
            subject=f"Resolved: Your support request for {real_order_ref} has been approved [{ticket_id}]",
            ticket_details=ticket_details
        )
    else:
        outcome = "Escalated"
        resolution_text = "Query requires manual agent verification due to insufficient detail or policy exception."
        
        # 4. Trigger Person 4's Enterprise Integrations on escalation with REAL ticket data
        jira_res = create_jira_ticket(
            summary=f"Escalated Support Ticket: {category} ({real_order_ref})",
            description=f"Query: {query_text}\nOrder Reference: {real_order_ref}\nCustomer Email: {real_customer_email}\nConfidence: {base_confidence}%",
            priority="High"
        )
        if isinstance(jira_res, dict):
            jira_key = jira_res.get("jira_key", "SHOP-1042")
        else:
            jira_key = "SHOP-1042"

        ticket_details = {
            "jira_key": jira_key,
            "category": category,
            "priority": "High",
            "order_ref": real_order_ref,
            "customer_email": real_customer_email,
            "customer_name": extract_customer_name(real_customer_email, "Yashwanth"),
            "created_at": created_at_str,
            "query_text": query_text,
            "resolution_draft": resolution_text,
            "jira_browse_url": f"{os.getenv('JIRA_URL', 'https://yashwanthaagunuri12.atlassian.net').rstrip('/')}/browse/{jira_key}"
        }

        send_escalation_email(
            recipient_email=real_customer_email,
            subject=f"Action Required: Your support ticket has been escalated [{jira_key}]",
            body=f"A support ticket has been flagged for manual review.\n\nQuery: {query_text}\nConfidence Score: {base_confidence}%\nJira Ticket ID: {jira_key}",
            ticket_details=ticket_details
        )

    return {
        "matched_policy": matched_policy,
        "confidence": f"{base_confidence}%",
        "outcome": outcome,
        "resolution": resolution_text,
        "jira_key": jira_key or ticket_id,
        "ticket_id": ticket_id or jira_key,
        "email_sent": True
    }