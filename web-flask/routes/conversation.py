import json
import os
from flask import Blueprint, request, jsonify, current_app

from algo.knowledge_graph.triplet_extractor import extract_entities
from algo.knowledge_graph.graph_retriever import retrieve_knowledge
from algo.knowledge_graph.context_builder import build_context
from algo.llm.llm_client import SiliconFlowLLM
from algo.llm.prompt_builder import build_prompt

bp = Blueprint("conversation", __name__, url_prefix="/chat")

llm = None  # 延迟初始化

def load_llm_config():
    config_path = os.path.join(current_app.root_path, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config["siliconflow"]

def get_llm():
    global llm
    if llm is None:
        cfg = load_llm_config()
        llm = SiliconFlowLLM(
            api_key=cfg["api_key"],
            base_url=cfg["base_url"],
            model=cfg["model"],
            timeout=cfg.get("timeout", 30)
        )
    return llm

@bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "question 不能为空"}), 400

    question = data["question"]

    # GraphRAG 主流程
    entities = extract_entities(question)
    graph_data = retrieve_knowledge(entities)
    context = build_context(graph_data)
    prompt = build_prompt(question, context)

    answer = get_llm().chat(prompt)

    return jsonify({
        "answer": answer,
        "context": context
    })
