from flask import Blueprint, request, jsonify
from algo.knowledge_graph.triplet_extractor import extract_entities
from algo.knowledge_graph.graph_retriever import retrieve_knowledge
from algo.knowledge_graph.context_builder import build_context

bp = Blueprint("knowledge_graph", __name__, url_prefix="/kg")

@bp.route("/query", methods=["POST"])
def query_kg():
    data = request.get_json(silent=True)

    if not data or "question" not in data:
        return jsonify({"error": "question 不能为空"}), 400

    question = data["question"]

    entities = extract_entities(question)
    graph_data = retrieve_knowledge(entities)
    context = build_context(graph_data)

    return jsonify({
        "entities": entities,
        "graph_data": graph_data,
        "context": context
    })
