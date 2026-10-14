
import re

MAX_RECENT_MESSAGES = 8
MAX_SUGGESTIONS = 3


def get_negotiation_suggestions(recent_messages, viewer_is_buyer=True):
    if not recent_messages:
        return []

    # Get the most recent message
    latest_message = recent_messages[-1]

    if not isinstance(latest_message, dict):
        return []

    latest_sender = latest_message.get("sender", "").lower()
    latest_text = str(latest_message.get("text", "")).lower().strip()

    # Do not generate suggestions if the latest message is empty
    if not latest_text:
        return []

    # Identify whether the latest message belongs to the current user
    current_role = "buyer" if viewer_is_buyer else "seller"

    # Only show suggestions when the other person sent the latest message.
    # This prevents responding to your own message with suggestions.
    if latest_sender == current_role:
        return []

    suggestions = []

    def add(label, action, reason):
        if not any(s["action"] == action for s in suggestions):
            suggestions.append({
                "label": label,
                "action": action,
                "reason": reason
            })

    # Buyer-specific suggestions
    if viewer_is_buyer:
        if re.search(
            r"\b(available|availability|still have|in stock)\b",
            latest_text
        ):
            add(
                "Ask about condition",
                "ask_condition",
                "Ask the seller about the item's condition."
            )

        if re.search(
            r"\b(condition|scratches|damaged|working|repair|defect)\b",
            latest_text
        ):
            add(
                "Negotiate price",
                "negotiate_price",
                "Prepare a polite price offer."
            )

        if re.search(
            r"\b(price|budget|offer|discount|cheaper|negotiate|expensive)\b",
            latest_text
        ):
            add(
                "Draft an offer",
                "draft_offer",
                "Prepare an offer for the seller."
            )

        if not suggestions:
            add(
                "Compare prices",
                "compare_prices",
                "Compare this item with similar marketplace listings."
            )

    # Seller-specific suggestions
    else:
        if re.search(
            r"\b(price|budget|offer|discount|cheaper|negotiate|expensive)\b",
            latest_text
        ):
            add(
                "Draft a counteroffer",
                "draft_counteroffer",
                "Prepare a polite counteroffer for the buyer."
            )

        if re.search(
            r"\b(condition|scratches|damaged|working|repair|defect)\b",
            latest_text
        ):
            add(
                "Explain item condition",
                "clarify_next_steps",
                "Prepare a clear response about the item."
            )

        if re.search(
            r"\b(pickup|pick up|delivery|finalise|finalize|purchase)\b",
            latest_text
        ):
            add(
                "Clarify next steps",
                "clarify_next_steps",
                "Confirm pickup or the next transaction step."
            )

    return suggestions[:MAX_SUGGESTIONS]
