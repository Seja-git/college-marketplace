from flask import request, jsonify, render_template
from flask_login import login_required

from app.copilot.agent import get_copilot_response
from app.copilot.tools.listing_tools import (
    generate_listing_assistance
)

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
    