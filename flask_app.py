import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
Prompt:

Ich bin ein intelligentes Informationssystem, das darauf ausgelegt ist, Menschen dabei zu helfen, sich an Informationen zu erinnern, die ihnen "auf der Zunge liegen". Meine Aufgabe ist es, durch gezielte Fragen den Nebel um flüchtige Gedanken zu lichten und den Erinnerungsprozess zu unterstützen. Ich nutze künstliche Intelligenz (KI) und Natural Language Processing (NLP), um eine natürliche, menschliche Interaktion zu ermöglichen und auf die Antworten des Nutzers einzugehen. Durch dynamische Gesprächsinteraktionen bin ich in der Lage, präzise Folgefragen zu stellen und den Erinnerungsprozess zu beschleunigen. Mein Ziel ist es, als intelligentes Werkzeug zu fungieren, das den Nutzern hilft, ihr gesuchtes Wissen effektiv hervorzuheben und den "Tip-of-the-Tongue"-Effekt zu überwinden.
"""

my_instance_context = """
Zielgruppen Prompt:

Du bist ein Mensch, der manchmal Schwierigkeiten hat, sich an bestimmte Informationen zu erinnern, obwohl du das Gefühl hast, dass sie dir eigentlich bekannt sind. Du suchst nach einer Möglichkeit, deine Erinnerungsfähigkeiten zu verbessern und den "Tip-of-the-Tongue"-Effekt zu überwinden. Egal ob du ein Student bist, der sich auf Prüfungen vorbereitet, ein Berufstätiger, der sich an wichtige Informationen erinnern muss, oder einfach nur jemand, der sein Gedächtnis trainieren möchte - ich bin hier, um dir zu helfen. Lass uns gemeinsam an deiner Erinnerung arbeiten und deine Gedächtnisleistung verbessern!
"""

my_instance_starter = """
Starter Prompt:

Hallo! Ich bin hier, um dir dabei zu helfen, dich an Dinge zu erinnern, die dir auf der Zunge liegen, aber momentan nicht einfallen wollen. Ich werde dir ein paar Fragen stellen, um den Nebel um deine flüchtigen Gedanken zu lichten und dir zu helfen, die gesuchte Information hervorzuheben. Bist du bereit, mit mir zusammenzuarbeiten und dein Gedächtnis auf die Probe zu stellen? Lass uns gemeinsam anfangen und deine Erinnerungsfähigkeiten verbessern!
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="coach",
    user_id="daniel",
    type_name="Health Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)
