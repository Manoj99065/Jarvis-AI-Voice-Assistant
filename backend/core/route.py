# from flask import request, jsonify, send_from_directory, g
# from backend.command.dispatcher import handle_command, handle_followup
# from backend.utils.helpers import wishMe

# # We'll store pending follow‑up in Flask's g object (per request)
# # For persistent session, we could use session, but we'll use a simple global dict.
# # Since g is request-scoped, we need to store pending across requests – use a dict keyed by session id.
# # For simplicity, we'll store in a global dictionary (not thread-safe but works for demo).
# pending_actions = {}

# def register_routes(app):
#     @app.route('/')
#     def index():
#         return send_from_directory('../../frontend', 'index.html')

#     @app.route('/<path:filename>')
#     def static_files(filename):
#         return send_from_directory('../../frontend', filename)

#     @app.route('/api/command', methods=['POST'])
#     def command():
#         data = request.get_json()
#         query = data.get('query', '').lower().strip()
#         if not query:
#             return jsonify({"error": "No query provided"}), 400

#         # Use a simple session ID (e.g., IP or a cookie) – for demo we use a fixed key
#         # In production, use Flask session.
#         session_id = request.remote_addr  # not perfect, but okay for demo
#         pending = pending_actions.get(session_id)

#         if pending:
#             action = pending.get("action")
#             # data could be the original data
#             reply = handle_followup(action, pending.get("data"), query)
#             pending_actions.pop(session_id, None)
#             return jsonify({"reply": reply})

#         response = handle_command(query)

#         # If the response asks for a follow‑up, store it
#         if response.get("action") == "ask_followup":
#             pending_actions[session_id] = {
#                 "action": response.get("data"),
#                 "data": response.get("data")   # store the context
#             }

#         return jsonify(response)

#     @app.route('/api/greeting', methods=['GET'])
#     def greeting():
#         return jsonify({"greeting": wishMe()})



from flask import request, jsonify, send_from_directory, g
from backend.command.dispatcher import handle_command, handle_followup
from backend.utils.helpers import wishMe

pending_actions = {}

def register_routes(app):
    @app.route('/')
    def index():
        return send_from_directory('../../frontend', 'index.html')

    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory('../../frontend', filename)

    @app.route('/api/command', methods=['POST'])
    def command():
        data = request.get_json()
        query = data.get('query', '').strip()  # ⚠️ .lower() hata do yahan
        if not query:
            return jsonify({"error": "No query provided"}), 400

        session_id = request.remote_addr
        pending = pending_actions.get(session_id)

        if pending:
            action = pending.get("action")
            reply = handle_followup(action, pending.get("data"), query)
            pending_actions.pop(session_id, None)
            return jsonify({"reply": reply})

        response = handle_command(query)

        if response.get("action") == "ask_followup":
            pending_actions[session_id] = {
                "action": response.get("data"),
                "data": response.get("data")
            }

        return jsonify(response)

    @app.route('/api/greeting', methods=['GET'])
    def greeting():
        return jsonify({"greeting": wishMe()})