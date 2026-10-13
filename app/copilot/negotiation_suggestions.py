
import re


MAX_RECENT_MESSAGES = 8
MAX_SUGGESTIONS = 3


def get_negotiation_suggestions(recent_messages, viewer_is_buyer=True):
    """Return chat suggestions without calling Gemini."""

    if not recent_messages:
        return []

    text = " ".join(
        str(message.get("text", ""))
        for message in recent_messages[-MAX_RECENT_MESSAGES:]
        if isinstance(message, dict)
    ).lower()

    if not text.strip():
        return []

    suggestions = []

    def add(label, action, reason):
        if not any(s["action"] == action for s in suggestions):
            suggestions.append({
                "label": label,
                "action": action,
                "reason": reason,
            })

    if viewer_is_buyer and re.search(
        r"\b(available|availability|still have|in stock)\b", text
    ):
        add(
            "Ask about condition",
            "ask_condition",
            "Learn more about the item's condition.",
        )

    if re.search(
        r"\b(condition|scratches|damaged|working|repair|defect)\b", text
    ) and viewer_is_buyer:
        add(
            "Negotiate price",
            "negotiate_price",
            "Prepare a polite price offer.",
        )

    if re.search(
        r"\b(price|budget|offer|discount|cheaper|negotiate|expensive)\b",
        text,
    ):
        if viewer_is_buyer:
            add(
                "Draft an offer",
                "draft_offer",
                "Prepare an offer for the seller.",
            )
        else:
            add(
                "Draft a counteroffer",
                "draft_counteroffer",
                "Prepare a counteroffer for the buyer.",
            )

    if re.search(
        r"\b(pickup|pick up|delivery|finalise|finalize|purchase)\b", text
    ):
        add(
            "Clarify next steps",
            "clarify_next_steps",
            "Confirm the next step in the transaction.",
        )

    if not suggestions and viewer_is_buyer:
        add(
            "Compare prices",
            "compare_prices",
            "Check similar marketplace listings.",
        )

    return suggestions[:MAX_SUGGESTIONS]