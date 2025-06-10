import webbrowser
import time
import keyring
import logging

from multiprocessing import Process, Event
from flask import Flask, render_template, request, jsonify

logger = logging.getLogger(__name__)

class MicroServer:
    def __init__(self, app_id, environment):
        self._app_id = app_id
        self._environment = environment
        self._app = Flask(__name__)
        self._token_received_event = Event()
        self._register_routes()

    def connect_account(self):
        flask_process = Process(target=self._app.run)
        flask_process.start()
        webbrowser.open("http://127.0.0.1:5000")
        self._token_received_event.wait()
        time.sleep(.5)
        flask_process.terminate()
        flask_process.join()

    def _register_routes(self):

        @self._app.route("/", methods=["GET"])
        def home():
            return render_template("index.html")

        @self._app.route("/complete", methods=["POST"])
        def complete():
            access_token = request.get_json().get("access_token", None)
            if access_token:
                keyring.set_password("bank-fetch", "default", access_token)
                self._token_received_event.set()
                logger.info("Access token received successfully from web UI")
                return "Access token received. You may now close this window."
            else:
                return "No access token received.", 400

        @self._app.route("/app", methods=["GET"])
        def get_app_info():
            logger.debug("App data requested from webserver")
            data = {
                "app_id": self._app_id,
                "environment": self._environment,
            }
            return jsonify(data)

        # appease the LSP gods
        _ = get_app_info, complete, home
