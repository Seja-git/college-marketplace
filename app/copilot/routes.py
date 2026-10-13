

from app.copilot.agent import get_copilot_response
from app.copilot.tools.listing_tools import (
    generate_listing_assistance
)

from flask import jsonify, request, abort, render_template
from flask_login import current_user, login_required

from app.models import Conversation
from app.copilot.negotiation_suggestions import (
    get_negotiation_suggestions,
)
from app.copilot.negotiation_drafts import (
    generate_negotiation_draft,
)
from app.copilot.tools.price_tools import compare_product_prices
def register_copilot_routes(app):

    # ---------------------------------------------------------
    # COPILOT PAGE
    # ---------------------------------------------------------

    @app.route("/copilot")
    @login_required
    def copilot_page():

        return render_template("copilot.html")


    # ---------------------------------------------------------
    # COPILOT CHAT API
    # ---------------------------------------------------------

    @app.route("/copilot/chat", methods=["POST"])
    @login_required
    def copilot_chat():

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "Request body is required."
            }), 400


        user_message = data.get(
            "message",
            ""
        ).strip()


        if not user_message:

            return jsonify({
                "success": False,
                "error": "Message cannot be empty."
            }), 400


        try:

            response = get_copilot_response(
                user_message
            )


            return jsonify({
                "success": True,
                "response": response
            })


        except Exception as e:

            print(
                "Copilot Error:",
                e
            )


            return jsonify({
                "success": False,
                "error": "Unable to process your request right now."
            }), 500


    @app.route(
    "/copilot/generate-listing",
    methods=["POST"]
  )
    @login_required
    def generate_listing():

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        product_info = data.get(
            "product_info",
            ""
        ).strip()

        if not product_info:
            return jsonify({
                "success": False,
                "message": "Please describe your product."
            }), 400
        result = generate_listing_assistance(
                product_info
            )
    
        if not result.get("success"):
                return jsonify(result), 500
        
        return jsonify(result)


    
    def get_authorized_conversation(conversation_id):
        conversation = Conversation.query.get_or_404(conversation_id)

        if current_user.id not in (
            conversation.buyer_id,
            conversation.seller_id,
        ):
            abort(403)

        return conversation

    def get_recent_chat_context(conversation):
        messages = conversation.messages[-8:]
        context = []

        for message in messages:
            if message.sender_id == conversation.buyer_id:
                sender = "buyer"
            else:
                sender = "seller"

            context.append({
                "sender": sender,
                "text": message.message,
            })

        return context

    @app.route(
        "/copilot/conversations/<int:conversation_id>/suggestions",
        methods=["GET"],
    )
    @login_required
    def negotiation_suggestions(conversation_id):
        conversation = get_authorized_conversation(conversation_id)

        recent_messages = get_recent_chat_context(conversation)

        suggestions = get_negotiation_suggestions(
            recent_messages,
            viewer_is_buyer=(
                current_user.id == conversation.buyer_id
            ),
        )

        return jsonify({"suggestions": suggestions})

    @app.route(
        "/copilot/conversations/<int:conversation_id>/draft",
        methods=["POST"],
    )
    @login_required
    def negotiation_draft(conversation_id):
        conversation = get_authorized_conversation(conversation_id)

        data = request.get_json(silent=True) or {}
        action = data.get("action")

        recent_messages = get_recent_chat_context(conversation)
        item = conversation.item

        if action == "compare_prices":
            try:
                comparison = compare_product_prices(item.title)
                return jsonify({
                    "type": "comparison",
                    "comparison": comparison,
                })
            except Exception:
                app.logger.exception("Price comparison failed")
                return jsonify({
                    "error": "Price comparison is temporarily unavailable."
                }), 503

        if action not in {
            "ask_condition",
            "negotiate_price",
            "draft_offer",
            "draft_counteroffer",
            "clarify_next_steps",
        }:
            return jsonify({"error": "Invalid suggestion."}), 400

        # Retrieve comparable listing data only for price negotiation.
        comparison = None

        if action in {
            "negotiate_price",
            "draft_offer",
            "draft_counteroffer",
        }:
            try:
                comparison = compare_product_prices(item.title)
            except Exception:
                # Drafting can still work without price comparisons.
                app.logger.exception(
                    "Could not retrieve comparable listing prices"
                )

        try:
            result = generate_negotiation_draft(
                action=action,
                item_title=item.title,
                listed_price=item.price,
                recent_messages=recent_messages,
                price_comparison=comparison,
            )

            return jsonify({
                "type": "draft",
                **result,
            })

        except Exception:
            app.logger.exception("Negotiation draft request failed")
            return jsonify({
                "error": (
                    "Draft generation is temporarily unavailable. "
                    "Please try again."
                )
            }), 503
    