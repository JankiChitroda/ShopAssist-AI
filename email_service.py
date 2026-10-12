import os
import smtplib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def extract_customer_name(email_or_name, fallback="Valued Customer"):
    """Extracts a friendly capitalized first name from email or name string."""
    if not email_or_name:
        return fallback
    if "@" not in email_or_name:
        return email_or_name.strip().title()
    prefix = email_or_name.split("@")[0]
    cleaned = re.sub(r"\d+", "", prefix)
    parts = re.split(r"[\._\-+]", cleaned)
    parts = [p.capitalize() for p in parts if p]
    if parts:
        first = parts[0]
        if first.lower().startswith("yashwanth"):
            return "Yashwanth"
        return " ".join(parts)
    return fallback

def build_escalation_email_html(data):
    """
    Builds the pixel-perfect, responsive HTML email matching the exact ShopAssist 
    side-by-side edition from your screenshot.
    """
    jira_key = data.get("jira_key") or "SHOP-6"
    category = data.get("category") or "Payment Dispute"
    priority = data.get("priority") or "High"
    order_ref = data.get("order_ref") or "#ORD-7741"
    customer_email = data.get("customer_email") or os.getenv("SMTP_EMAIL", "yashwanthaagunuri15@gmail.com")
    customer_name = data.get("customer_name") or extract_customer_name(customer_email, "Yashwanth")
    created_at = data.get("created_at") or datetime.now().strftime("%b %d, %Y, %I:%M %p")
    query_text = data.get("query_text") or "I was charged twice for order #ORD-7741 and need immediate supervisor review."
    resolution_draft = data.get("resolution_draft") or data.get("resolution") or "Query requires manual verification."
    
    jira_base = os.getenv("JIRA_URL", "https://yashwanthaagunuri12.atlassian.net").rstrip("/")
    jira_url = data.get("jira_browse_url") or f"{jira_base}/browse/{jira_key}"
    
    cat_lower = category.lower().strip()
    if "dispute" in cat_lower or "payment" in cat_lower:
        cat_phrase = "payment dispute"
    elif "return" in cat_lower or "refund" in cat_lower:
        cat_phrase = "returns and refunds request"
    elif "delivery" in cat_lower or "order" in cat_lower:
        cat_phrase = "order delivery inquiry"
    elif "damaged" in cat_lower:
        cat_phrase = "damaged item report"
    else:
        cat_phrase = f"{cat_lower} inquiry"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>Your support ticket has been escalated</title>
<style type="text/css">
  body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
  table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
  img {{ -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; }}
  table {{ border-collapse: collapse !important; }}
  body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; }}

  @media only screen and (max-width: 620px) {{
    .outer-body {{ padding: 10px 4px !important; }}
    .main-card {{ padding: 20px 12px 18px 12px !important; border-radius: 14px !important; }}
    .action-banner {{ padding: 14px 12px !important; }}
    .action-title {{ font-size: 16px !important; }}
    .action-sub {{ font-size: 11.5px !important; }}
    .details-box {{ padding: 14px 10px !important; }}
    .badge-pill {{ font-size: 10px !important; padding: 3px 8px !important; }}
    .left-col {{ padding-right: 8px !important; }}
    .right-col {{ padding-left: 10px !important; }}
    .specs-table {{ font-size: 10.5px !important; }}
    .specs-label {{ font-size: 10px !important; }}
    .specs-val {{ font-size: 10.5px !important; }}
    .step-desc {{ font-size: 9.5px !important; }}
    .step-title {{ font-size: 11px !important; }}
  }}
</style>
</head>
<body class="outer-body" style="margin: 0; padding: 20px 10px; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #0f172a;">

<!-- Center Container -->
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed;">
  <tr>
    <td align="center">
      
      <!-- Main Card Matching Screenshot -->
      <table width="100%" border="0" cellspacing="0" cellpadding="0" class="main-card" style="max-width: 640px; background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 25px rgba(15, 23, 42, 0.06); padding: 32px 30px 26px 30px; table-layout: fixed;">
        
        <!-- Header -->
        <tr>
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 22px;">
              <tr>
                <td align="left" valign="middle">
                  <table border="0" cellspacing="0" cellpadding="0">
                    <tr>
                      <td valign="middle" style="padding-right: 10px;">
                        <div style="width: 38px; height: 38px; background-color: #0052cc; border-radius: 10px; text-align: center; line-height: 38px;">
                          <span style="color: #ffffff; font-size: 20px;">&#128722;</span>
                        </div>
                      </td>
                      <td valign="middle">
                        <div style="font-size: 22px; font-weight: 800; color: #0052cc; letter-spacing: -0.4px; line-height: 1.1;">ShopAssist</div>
                        <div style="font-size: 11px; color: #64748b; font-weight: 500; margin-top: 2px;">Shop Smarter. We're Here to Help.</div>
                      </td>
                    </tr>
                  </table>
                </td>
                <td align="right" valign="middle">
                  <a href="{jira_url}" target="_blank" style="color: #0052cc; font-size: 13px; font-weight: 700; text-decoration: none;">Visit Dashboard &rarr;</a>
                  <div style="font-size: 11px; color: #94a3b8; margin-top: 3px;"><a href="mailto:shopassist23@gmail.com" style="color: #94a3b8; text-decoration: none;">Help Center</a> &nbsp;&bull;&nbsp; <a href="mailto:shopassist23@gmail.com" style="color: #0052cc; text-decoration: none; font-weight: 600;">Contact Support</a></div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Alert Banner Card (Red/Pink Action Required Box) -->
        <tr>
          <td>
            <div class="action-banner" style="background: linear-gradient(135deg, #fff5f5 0%, #fee2e2 100%); border: 1px solid #fecaca; border-radius: 16px; padding: 18px 22px; margin-bottom: 22px;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td width="50" valign="middle" style="padding-right: 14px;">
                    <div style="width: 44px; height: 44px; background-color: #fee2e2; border: 1px solid #fca5a5; border-radius: 12px; text-align: center; line-height: 44px; font-size: 20px;">
                      &#9888;&#65039;
                    </div>
                  </td>
                  <td valign="middle">
                    <div style="font-size: 11px; font-weight: 800; color: #dc2626; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2px;">ACTION REQUIRED</div>
                    <div class="action-title" style="font-size: 18px; font-weight: 800; color: #0f172a; margin-bottom: 4px; letter-spacing: -0.3px;">Your support ticket has been escalated</div>
                    <div class="action-sub" style="font-size: 12.5px; color: #475569; line-height: 1.45;">Your {cat_phrase} requires additional verification, so we've escalated it to our Tier-2 Support Team for further review.</div>
                  </td>
                  <td width="56" align="right" valign="middle">
                    <div style="width: 48px; height: 48px; background-color: #ffe4e6; border: 1px solid #fecdd3; border-radius: 50%; text-align: center; line-height: 48px; font-size: 22px;">
                      &#128196;
                    </div>
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding-bottom: 18px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">Hello <span style="color: #0052cc;">{customer_name}</span>,</div>
            <div style="font-size: 13px; color: #475569; line-height: 1.55;">
              We wanted to inform you that your support ticket has been escalated to a human agent for further review. Our team will manually verify the details and get back to you as soon as possible.
            </div>
          </td>
        </tr>

        <!-- Ticket Details Card (SIDE-BY-SIDE EDITION) -->
        <tr>
          <td>
            <div class="details-box" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px 18px; margin-bottom: 22px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
              
              <!-- Card Header -->
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 16px; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px;">
                <tr>
                  <td align="left" valign="middle">
                    <table border="0" cellspacing="0" cellpadding="0">
                      <tr>
                        <td valign="middle" style="padding-right: 8px;">
                          <div style="width: 30px; height: 30px; background-color: #eff6ff; border-radius: 8px; text-align: center; line-height: 30px; font-size: 16px;">
                            &#128196;
                          </div>
                        </td>
                        <td valign="middle">
                          <div style="font-size: 15px; font-weight: 800; color: #0f172a;">Ticket Details</div>
                          <div style="font-size: 11px; color: #64748b;">Key information about your request</div>
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td align="right" valign="middle">
                    <div class="badge-pill" style="display: inline-block; background-color: #f3e8ff; border: 1px solid #e9d5ff; border-radius: 9999px; padding: 4px 10px; white-space: nowrap;">
                      <span style="color: #7e22ce; font-weight: 700; font-size: 11px; white-space: nowrap;">&uarr; Escalated to Tier-2 &nbsp;&bull;</span>
                    </div>
                  </td>
                </tr>
              </table>

              <!-- SIDE BY SIDE 2-COLUMN GRID (48% Left / 52% Right) -->
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed;">
                <tr>
                  <!-- Left Specs Column (48% Side-by-Side) -->
                  <td width="48%" valign="top" class="left-col" style="padding-right: 12px; width: 48%;">
                    <table width="100%" border="0" cellspacing="0" cellpadding="0" class="specs-table" style="font-size: 12px;">
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;"># &nbsp;Ticket ID</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0052cc; font-weight: 800; font-family: monospace; font-size: 13px; width: 58%;">{jira_key}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#127991;&#65039; &nbsp;Category</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0f172a; font-weight: 700; width: 58%;">{category}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#128202; &nbsp;Priority</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; width: 58%;">
                          <span style="display: inline-block; background-color: #fef2f2; color: #dc2626; border: 1px solid #fecaca; border-radius: 9999px; padding: 2px 9px; font-size: 10.5px; font-weight: 800; white-space: nowrap;">
                            &#9679; {priority}
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#128722; &nbsp;Order Reference</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0f172a; font-weight: 700; font-family: monospace; font-size: 12px; width: 58%;">{order_ref}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#9993;&#65039; &nbsp;Customer Email</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0f172a; font-weight: 600; font-size: 11px; word-break: break-word; overflow-wrap: break-word; width: 58%;">{customer_email}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#128197; &nbsp;Created At</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #475569; font-weight: 600; font-size: 11px; width: 58%;">{created_at}</td>
                      </tr>
                    </table>
                  </td>

                  <!-- Right Text Boxes (52%) -->
                  <td width="52%" valign="top" class="right-col" style="padding-left: 14px; border-left: 1px solid #f1f5f9; width: 52%;">
                    <!-- Your Query Box -->
                    <div style="margin-bottom: 12px;">
                      <div style="font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 5px;">
                        &#128172; &nbsp;Your Query
                      </div>
                      <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #334155; line-height: 1.45; word-break: break-word;">
                        {query_text}
                      </div>
                    </div>
                    <!-- Proposed Draft (AI) Box -->
                    <div>
                      <div style="font-size: 11.5px; font-weight: 700; color: #7e22ce; margin-bottom: 5px;">
                        &#10022; &nbsp;Proposed Draft (AI)
                      </div>
                      <div style="background-color: #faf5ff; border: 1px solid #f3e8ff; border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #581c87; line-height: 1.45; word-break: break-word;">
                        {resolution_draft}
                      </div>
                    </div>
                  </td>
                </tr>
              </table>

            </div>
          </td>
        </tr>

        <!-- What Happens Next? Stepper Card -->
        <tr>
          <td>
            <div class="details-box" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px 18px; margin-bottom: 22px;">
              <div style="font-size: 15px; font-weight: 800; color: #0f172a; margin-bottom: 18px;">What Happens Next?</div>
              
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 20px; table-layout: fixed;">
                <tr>
                  <!-- Step 1 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #eff6ff; border: 1px solid #dbeafe; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #2563eb; margin: 0 auto 6px auto;">&#128269;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Manual Review</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">Our support team will review your case.</div>
                  </td>
                  <!-- Step 2 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #eff6ff; border: 1px solid #dbeafe; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #2563eb; margin: 0 auto 6px auto;">&#128203;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Investigate</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">We will verify order and payment details.</div>
                  </td>
                  <!-- Step 3 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #eff6ff; border: 1px solid #dbeafe; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #2563eb; margin: 0 auto 6px auto;">&#9993;&#65039;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Update You</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">You'll receive an email with updates.</div>
                  </td>
                  <!-- Step 4 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #eff6ff; border: 1px solid #dbeafe; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #2563eb; margin: 0 auto 6px auto;">&#10004;&#65039;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Resolution</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">We'll work towards a fair resolution.</div>
                  </td>
                </tr>
              </table>

              <!-- Centered Blue CTA Button -->
              <div style="text-align: center; margin-bottom: 10px;">
                <a href="{jira_url}" target="_blank" style="display: inline-block; background-color: #0052cc; color: #ffffff; font-size: 13.5px; font-weight: 700; text-decoration: none; padding: 11px 28px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,82,204,0.25);">
                  View Ticket Details &rarr;
                </a>
              </div>
              <div style="text-align: center; font-size: 11.5px; color: #64748b;">
                You can also reply to this email or reach us directly at <a href="mailto:shopassist23@gmail.com" style="color: #0052cc; text-decoration: none; font-weight: 600;">shopassist23@gmail.com</a>
              </div>
            </div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-top: 1px solid #e2e8f0; padding-top: 16px; margin-top: 4px;">
              <tr>
                <td align="left" valign="middle">
                  <div style="font-size: 16px; font-weight: 800; color: #0052cc;">&#128722; ShopAssist</div>
                  <div style="font-size: 10px; color: #94a3b8; margin-top: 1px;">Shop Smarter. We're Here to Help.</div>
                </td>
                <td align="center" valign="middle">
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#127760;</span>
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#128247;</span>
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#128038;</span>
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#128188;</span>
                </td>
                <td align="right" valign="middle">
                  <div style="font-size: 10.5px; color: #64748b; font-weight: 600;">Need help?</div>
                  <a href="mailto:shopassist23@gmail.com" style="font-size: 10.5px; color: #0052cc; text-decoration: none; font-weight: 600;">shopassist23@gmail.com</a>
                </td>
              </tr>
            </table>
            <div style="text-align: center; font-size: 10.5px; color: #94a3b8; line-height: 1.45; margin-top: 14px;">
              This is an automated email from ShopAssist. Please do not share sensitive information such as your password or payment details via email.<br>
              &copy; 2026 ShopAssist. All rights reserved.
            </div>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

</body>
</html>"""

def send_escalation_email(recipient_email, subject, body, ticket_details=None):
    """
    Sends an SMTP email notification when a support ticket is escalated.
    Uses the exact side-by-side ShopAssist template matching your screenshot.
    Delivers directly to the email mentioned in Customer Identity,
    and sends a verified copy to the admin/operator inbox.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_EMAIL", "yashwanthaagunuri15@gmail.com")
    sender_password = os.getenv("SMTP_PASSWORD", "omxy apsl zrmx awde").replace(" ", "").strip()
    support_email = "shopassist23@gmail.com"
    admin_copy = os.getenv("ESCALATION_RECIPIENT", sender_email).strip()

    # Determine real customer email
    cust_email = (recipient_email or "").strip()
    if ticket_details and ticket_details.get("customer_email"):
        cust_email = ticket_details.get("customer_email").strip()

    # Build recipients list
    recipients = []
    if cust_email and "@" in cust_email and not cust_email.endswith("@shopassist.ai"):
        recipients.append(cust_email)
    
    # Always include the original support account and admin copy
    for sup_acc in [support_email, admin_copy, sender_email]:
        if sup_acc and sup_acc not in recipients:
            recipients.append(sup_acc)

    if not recipients:
        recipients = [sender_email]

    primary_to = cust_email if (cust_email and "@" in cust_email) else recipients[0]

    # Prepare ticket data for HTML template
    details = ticket_details.copy() if ticket_details else {}
    if not details.get("customer_email"):
        details["customer_email"] = primary_to
    if not details.get("customer_name"):
        details["customer_name"] = extract_customer_name(primary_to, "Yashwanth")
    
    html_content = build_escalation_email_html(details)

    msg = MIMEMultipart("alternative")
    msg['From'] = f"ShopAssist Support <{support_email}>"
    msg['To'] = primary_to
    msg['Reply-To'] = support_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        clean_password = sender_password.replace(" ", "").strip()
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
        server.starttls()
        server.login(sender_email, clean_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print(f"[EMAIL SERVICE] Side-by-side HTML Escalation email successfully sent to: {recipients}")
        return True
    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] Failed to send email to {recipients}: {e}")
        return False

def build_auto_resolved_email_html(data):
    """
    Builds the pixel-perfect, responsive side-by-side HTML email for
    Auto-Resolved / Approved tickets, matching the exact ShopAssist design.
    """
    ticket_id = data.get("ticket_id") or data.get("jira_key") or "SHOP-RES-7741"
    category = data.get("category") or "Returns & Refunds"
    priority = data.get("priority") or "Normal"
    status = data.get("status") or "Approved"
    order_ref = data.get("order_ref") or "#ORD-7741"
    customer_email = data.get("customer_email") or os.getenv("SMTP_EMAIL", "yashwanthaagunuri15@gmail.com")
    customer_name = data.get("customer_name") or extract_customer_name(customer_email, "Yashwanth")
    created_at = data.get("created_at") or datetime.now().strftime("%b %d, %Y, %I:%M %p")
    query_text = data.get("query_text") or "Can I return this Nordic Alpaca Cardigan after 18 days? The tag is still attached."
    resolution = data.get("resolution") or data.get("resolution_draft") or f"Based on store policy ({category}), your request is approved."
    confidence = data.get("confidence") or "96.4%"
    
    cat_lower = category.lower().strip()
    if "return" in cat_lower or "refund" in cat_lower:
        cat_phrase = "returns and refunds request"
    elif "delivery" in cat_lower or "order" in cat_lower:
        cat_phrase = "order delivery inquiry"
    elif "dispute" in cat_lower or "payment" in cat_lower:
        cat_phrase = "payment inquiry"
    elif "damaged" in cat_lower:
        cat_phrase = "damaged item verification"
    else:
        cat_phrase = f"{cat_lower} request"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>Your support request has been approved</title>
<style type="text/css">
  body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
  table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
  img {{ -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; }}
  table {{ border-collapse: collapse !important; }}
  body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; }}

  @media only screen and (max-width: 620px) {{
    .outer-body {{ padding: 10px 4px !important; }}
    .main-card {{ padding: 20px 12px 18px 12px !important; border-radius: 14px !important; }}
    .action-banner {{ padding: 14px 12px !important; }}
    .action-title {{ font-size: 16px !important; }}
    .action-sub {{ font-size: 11.5px !important; }}
    .details-box {{ padding: 14px 10px !important; }}
    .badge-pill {{ font-size: 10px !important; padding: 3px 8px !important; }}
    .left-col {{ padding-right: 8px !important; }}
    .right-col {{ padding-left: 10px !important; }}
    .specs-table {{ font-size: 10.5px !important; }}
    .specs-label {{ font-size: 10px !important; }}
    .specs-val {{ font-size: 10.5px !important; }}
    .step-desc {{ font-size: 9.5px !important; }}
    .step-title {{ font-size: 11px !important; }}
  }}
</style>
</head>
<body class="outer-body" style="margin: 0; padding: 20px 10px; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #0f172a;">

<!-- Center Container -->
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed;">
  <tr>
    <td align="center">
      
      <!-- Main Card Matching Screenshot -->
      <table width="100%" border="0" cellspacing="0" cellpadding="0" class="main-card" style="max-width: 640px; background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 25px rgba(15, 23, 42, 0.06); padding: 32px 30px 26px 30px; table-layout: fixed;">
        
        <!-- Header -->
        <tr>
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 22px;">
              <tr>
                <td align="left" valign="middle">
                  <table border="0" cellspacing="0" cellpadding="0">
                    <tr>
                      <td valign="middle" style="padding-right: 10px;">
                        <div style="width: 38px; height: 38px; background-color: #059669; border-radius: 10px; text-align: center; line-height: 38px;">
                          <span style="color: #ffffff; font-size: 20px;">&#128722;</span>
                        </div>
                      </td>
                      <td valign="middle">
                        <div style="font-size: 22px; font-weight: 800; color: #059669; letter-spacing: -0.4px; line-height: 1.1;">ShopAssist</div>
                        <div style="font-size: 11px; color: #64748b; font-weight: 500; margin-top: 2px;">Shop Smarter. We're Here to Help.</div>
                      </td>
                    </tr>
                  </table>
                </td>
                <td align="right" valign="middle">
                  <a href="mailto:shopassist23@gmail.com" style="color: #059669; font-size: 13px; font-weight: 700; text-decoration: none;">Help &amp; Support &rarr;</a>
                  <div style="font-size: 11px; color: #94a3b8; margin-top: 3px;"><a href="mailto:shopassist23@gmail.com" style="color: #94a3b8; text-decoration: none;">Help Center</a> &nbsp;&bull;&nbsp; <a href="mailto:shopassist23@gmail.com" style="color: #059669; text-decoration: none; font-weight: 600;">Contact Us</a></div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Alert Banner Card (Green/Emerald Auto-Resolved Box) -->
        <tr>
          <td>
            <div class="action-banner" style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 1px solid #bbf7d0; border-radius: 16px; padding: 18px 22px; margin-bottom: 22px;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td width="50" valign="middle" style="padding-right: 14px;">
                    <div style="width: 44px; height: 44px; background-color: #dcfce7; border: 1px solid #86efac; border-radius: 12px; text-align: center; line-height: 44px; font-size: 22px;">
                      &#10004;&#65039;
                    </div>
                  </td>
                  <td valign="middle">
                    <div style="font-size: 11px; font-weight: 800; color: #15803d; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2px;">AUTO-RESOLVED &bull; CONSENSUS VERIFIED</div>
                    <div class="action-title" style="font-size: 18px; font-weight: 800; color: #064e3b; margin-bottom: 4px; letter-spacing: -0.3px;">Your support request has been approved</div>
                    <div class="action-sub" style="font-size: 12.5px; color: #166534; line-height: 1.45;">Your {cat_phrase} for order {order_ref} has been validated with {confidence} confidence and automatically resolved.</div>
                  </td>
                  <td width="56" align="right" valign="middle">
                    <div style="width: 48px; height: 48px; background-color: #d1fae5; border: 1px solid #a7f3d0; border-radius: 50%; text-align: center; line-height: 48px; font-size: 22px;">
                      &#127881;
                    </div>
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding-bottom: 18px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">Hello <span style="color: #059669;">{customer_name}</span>,</div>
            <div style="font-size: 13px; color: #475569; line-height: 1.55;">
              We are pleased to inform you that your customer support request regarding order <strong>{order_ref}</strong> has been autonomously approved by our policy engine. Please find the verified resolution details below.
            </div>
          </td>
        </tr>

        <!-- Ticket Details Card (SIDE-BY-SIDE EDITION) -->
        <tr>
          <td>
            <div class="details-box" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px 18px; margin-bottom: 22px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
              
              <!-- Card Header -->
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 16px; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px;">
                <tr>
                  <td align="left" valign="middle">
                    <table border="0" cellspacing="0" cellpadding="0">
                      <tr>
                        <td valign="middle" style="padding-right: 8px;">
                          <div style="width: 30px; height: 30px; background-color: #ecfdf5; border-radius: 8px; text-align: center; line-height: 30px; font-size: 16px;">
                            &#128196;
                          </div>
                        </td>
                        <td valign="middle">
                          <div style="font-size: 15px; font-weight: 800; color: #0f172a;">Ticket Details</div>
                          <div style="font-size: 11px; color: #64748b;">Key information about your resolution</div>
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td align="right" valign="middle">
                    <div class="badge-pill" style="display: inline-block; background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 9999px; padding: 4px 10px; white-space: nowrap;">
                      <span style="color: #059669; font-weight: 700; font-size: 11px; white-space: nowrap;">&#10004; Auto-Resolved &nbsp;&bull;</span>
                    </div>
                  </td>
                </tr>
              </table>

              <!-- SIDE BY SIDE 2-COLUMN GRID (48% Left / 52% Right) -->
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed;">
                <tr>
                  <!-- Left Specs Column (48% Side-by-Side) -->
                  <td width="48%" valign="top" class="left-col" style="padding-right: 12px; width: 48%;">
                    <table width="100%" border="0" cellspacing="0" cellpadding="0" class="specs-table" style="font-size: 12px;">
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;"># &nbsp;Ticket ID</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #059669; font-weight: 800; font-family: monospace; font-size: 13px; width: 58%;">{ticket_id}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#127991;&#65039; &nbsp;Category</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0f172a; font-weight: 700; width: 58%;">{category}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#128202; &nbsp;Status</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; width: 58%;">
                          <span style="display: inline-block; background-color: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; border-radius: 9999px; padding: 2px 9px; font-size: 10.5px; font-weight: 800; white-space: nowrap;">
                            &#9679; {status}
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#128722; &nbsp;Order Reference</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0f172a; font-weight: 700; font-family: monospace; font-size: 12px; width: 58%;">{order_ref}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#9993;&#65039; &nbsp;Customer Email</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #0f172a; font-weight: 600; font-size: 11px; word-break: break-word; overflow-wrap: break-word; width: 58%;">{customer_email}</td>
                      </tr>
                      <tr>
                        <td class="specs-label" style="padding: 5px 0; color: #64748b; font-weight: 600; white-space: nowrap; width: 42%;">&#128197; &nbsp;Resolved At</td>
                        <td class="specs-val" style="padding: 5px 0; padding-left: 6px; color: #475569; font-weight: 600; font-size: 11px; width: 58%;">{created_at}</td>
                      </tr>
                    </table>
                  </td>

                  <!-- Right Text Boxes (52%) -->
                  <td width="52%" valign="top" class="right-col" style="padding-left: 14px; border-left: 1px solid #f1f5f9; width: 52%;">
                    <!-- Your Query Box -->
                    <div style="margin-bottom: 12px;">
                      <div style="font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 5px;">
                        &#128172; &nbsp;Your Query
                      </div>
                      <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #334155; line-height: 1.45; word-break: break-word;">
                        {query_text}
                      </div>
                    </div>
                    <!-- Approved Resolution Box -->
                    <div>
                      <div style="font-size: 11.5px; font-weight: 700; color: #059669; margin-bottom: 5px;">
                        &#10004;&#65039; &nbsp;Approved Resolution
                      </div>
                      <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #166534; line-height: 1.45; word-break: break-word;">
                        {resolution}
                      </div>
                    </div>
                  </td>
                </tr>
              </table>

            </div>
          </td>
        </tr>

        <!-- What Happens Next? Stepper Card -->
        <tr>
          <td>
            <div class="details-box" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px 18px; margin-bottom: 22px;">
              <div style="font-size: 15px; font-weight: 800; color: #0f172a; margin-bottom: 18px;">What Happens Next?</div>
              
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 20px; table-layout: fixed;">
                <tr>
                  <!-- Step 1 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #059669; margin: 0 auto 6px auto;">&#128269;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Policy Match</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">Verified store policy match.</div>
                  </td>
                  <!-- Step 2 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #059669; margin: 0 auto 6px auto;">&#10004;&#65039;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Approved</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">Autonomous waiver granted.</div>
                  </td>
                  <!-- Step 3 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #059669; margin: 0 auto 6px auto;">&#128230;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Processing</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">Initiated fulfillment action.</div>
                  </td>
                  <!-- Step 4 -->
                  <td width="25%" align="center" valign="top" style="padding: 0 3px;">
                    <div style="width: 34px; height: 34px; background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 50%; text-align: center; line-height: 34px; font-size: 14px; color: #059669; margin: 0 auto 6px auto;">&#9993;&#65039;</div>
                    <div class="step-title" style="font-size: 11.5px; font-weight: 800; color: #0f172a;">Completed</div>
                    <div class="step-desc" style="font-size: 10px; color: #64748b; line-height: 1.35; margin-top: 3px;">Tracking updates sent via mail.</div>
                  </td>
                </tr>
              </table>

              <!-- Centered Green CTA Button -->
              <div style="text-align: center; margin-bottom: 10px;">
                <a href="mailto:shopassist23@gmail.com" style="display: inline-block; background-color: #059669; color: #ffffff; font-size: 13.5px; font-weight: 700; text-decoration: none; padding: 11px 28px; border-radius: 8px; box-shadow: 0 2px 8px rgba(5,150,105,0.25);">
                  Contact Support Team &rarr;
                </a>
              </div>
              <div style="text-align: center; font-size: 11.5px; color: #64748b;">
                You can also reply to this email or reach us directly at <a href="mailto:shopassist23@gmail.com" style="color: #059669; text-decoration: none; font-weight: 600;">shopassist23@gmail.com</a>
              </div>
            </div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-top: 1px solid #e2e8f0; padding-top: 16px; margin-top: 4px;">
              <tr>
                <td align="left" valign="middle">
                  <div style="font-size: 16px; font-weight: 800; color: #059669;">&#128722; ShopAssist</div>
                  <div style="font-size: 10px; color: #94a3b8; margin-top: 1px;">Shop Smarter. We're Here to Help.</div>
                </td>
                <td align="center" valign="middle">
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#127760;</span>
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#128247;</span>
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#128038;</span>
                  <span style="font-size: 13px; color: #64748b; margin: 0 4px;">&#128188;</span>
                </td>
                <td align="right" valign="middle">
                  <div style="font-size: 10.5px; color: #64748b; font-weight: 600;">Need help?</div>
                  <a href="mailto:shopassist23@gmail.com" style="font-size: 10.5px; color: #059669; text-decoration: none; font-weight: 600;">shopassist23@gmail.com</a>
                </td>
              </tr>
            </table>
            <div style="text-align: center; font-size: 10.5px; color: #94a3b8; line-height: 1.45; margin-top: 14px;">
              This is an automated resolution email from ShopAssist AI Operations.<br>
              &copy; 2026 ShopAssist. All rights reserved.
            </div>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

</body>
</html>"""

def send_auto_resolved_email(recipient_email, subject, ticket_details=None):
    """
    Sends an SMTP email notification when a ticket is automatically resolved by the AI.
    Uses the side-by-side ShopAssist template with the Auto-Resolved / Approved theme.
    Delivers directly to the email mentioned in Customer Identity,
    and sends a verified copy to the support account and admin.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_EMAIL", "yashwanthaagunuri15@gmail.com")
    sender_password = os.getenv("SMTP_PASSWORD", "omxy apsl zrmx awde").replace(" ", "").strip()
    support_email = "shopassist23@gmail.com"
    admin_copy = os.getenv("ESCALATION_RECIPIENT", sender_email).strip()

    # Determine real customer email
    cust_email = (recipient_email or "").strip()
    if ticket_details and ticket_details.get("customer_email"):
        cust_email = ticket_details.get("customer_email").strip()

    # Build recipients list
    recipients = []
    if cust_email and "@" in cust_email and not cust_email.endswith("@shopassist.ai"):
        recipients.append(cust_email)
    
    # Always include the original support account and admin copy
    for sup_acc in [support_email, admin_copy, sender_email]:
        if sup_acc and sup_acc not in recipients:
            recipients.append(sup_acc)

    if not recipients:
        recipients = [sender_email]

    primary_to = cust_email if (cust_email and "@" in cust_email) else recipients[0]

    details = ticket_details.copy() if ticket_details else {}
    if not details.get("customer_email"):
        details["customer_email"] = primary_to
    if not details.get("customer_name"):
        details["customer_name"] = extract_customer_name(primary_to, "Yashwanth")

    plain_body = (
        f"Dear {details['customer_name']},\n\n"
        f"Your customer support request regarding order reference '{details.get('order_ref', '#ORD-7741')}' has been autonomously approved by ShopAssist AI.\n\n"
        f"--- RESOLUTION DETAILS ---\n"
        f"{details.get('resolution', '')}\n\n"
        f"Category: {details.get('category', 'Support')}\n"
        f"Status: Approved\n\n"
        f"If you need any further assistance, feel free to reply directly to this email or reach us at {support_email}.\n\n"
        f"Best regards,\n"
        f"ShopAssist AI Customer Operations Team"
    )

    html_content = build_auto_resolved_email_html(details)

    msg = MIMEMultipart("alternative")
    msg['From'] = f"ShopAssist AI <{support_email}>"
    msg['To'] = primary_to
    msg['Reply-To'] = support_email
    msg['Subject'] = subject

    msg.attach(MIMEText(plain_body, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        clean_password = sender_password.replace(" ", "").strip()
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
        server.starttls()
        server.login(sender_email, clean_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print(f"[EMAIL SERVICE] Side-by-side Auto-Resolved HTML email successfully sent to: {recipients}")
        return True
    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] Failed to send auto-resolved email to {recipients}: {e}")
        return False

def send_resolution_email(recipient_email, order_ref, resolution, ticket_details=None):
    """
    Sends an SMTP email notification to the customer with their approved resolution.
    Triggered by the 'Dispatch Response' button in the UI or direct API.
    """
    details = ticket_details.copy() if ticket_details else {}
    if order_ref and not details.get("order_ref"):
        details["order_ref"] = order_ref
    if resolution and not details.get("resolution"):
        details["resolution"] = resolution
    if recipient_email and not details.get("customer_email"):
        details["customer_email"] = recipient_email

    ticket_id = details.get("ticket_id") or f"SHOP-RES-{str(order_ref or '7741').replace('#', '').replace('ORD-', '')}"
    details["ticket_id"] = ticket_id
    subject = f"Support Resolution Approved: Order {order_ref or 'Inquiry'} [{ticket_id}]"

    return send_auto_resolved_email(
        recipient_email=recipient_email,
        subject=subject,
        ticket_details=details
    )