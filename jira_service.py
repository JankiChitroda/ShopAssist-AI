import requests
import json

def create_jira_ticket(summary, description, priority="Medium"):
    """
    Creates a Jira task when a customer ticket requires human intervention.
    For local development/demos, this can simulate the API call or log the payload.
    """
    # Example Jira REST API integration structure (update with your actual domain/credentials if needed)
    jira_url = "https://your-domain.atlassian.net/rest/api/2/issue"
    
    payload = {
        "fields": {
            "project": {"key": "SHOP"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
            "priority": {"name": priority}
        }
    }
    
    # For presentation purposes, we'll log it and return a success mock
    print(f"[JIRA INTEGRATION] Created ticket: {summary} [Priority: {priority}]")
    return {
        "status": "success",
        "jira_key": "SHOP-1042",
        "message": "Jira ticket successfully logged for human review."
    }