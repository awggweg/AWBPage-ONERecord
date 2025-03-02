from flask import Flask, request, jsonify
from flask_cors import CORS
from rdflib import Graph
from rdflib.plugins.sparql import processUpdate
import json

app = Flask(__name__)

CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:3000"}})

def jsonld_to_rdf_graph(jsonld_data):
    """将 JSON-LD 数据转换为 RDF 图"""
    graph = Graph()
    graph.parse(data=json.dumps(jsonld_data), format='json-ld')
    return graph

def execute_sparql_query(graph, sparql_query):
    """执行 SPARQL 查询并返回 JSON 序列化结果"""
    results = graph.query(sparql_query)
    
    # 将 SPARQL 结果转换为 JSON 格式
    if results.type == 'SELECT':
        return [{
            str(var): str(val) 
            for var, val in row.asdict().items()
        } for row in results]
    elif results.type == 'CONSTRUCT':
        # 如果是 CONSTRUCT 查询，返回三元组列表
        return [
            {
                "subject": str(triple[0]),
                "predicate": str(triple[1]),
                "object": str(triple[2])
            } 
            for triple in results
        ]
    else:
        return []

@app.route('/query', methods=['POST'])
def handle_query():
    # 校验请求数据格式
    data = request.get_json()
    if not data or 'sparql' not in data or 'jsonld' not in data:
        return jsonify({"error": "Missing 'sparql' or 'jsonld' in request body"}), 400

    try:
        # 1. 解析 JSON-LD 并转换为 RDF 图
        graph = jsonld_to_rdf_graph(data['jsonld'])
        # 打印 RDF 图到控制台
        print(graph.serialize(format='turtle'))
        # 2. 执行 SPARQL 查询
        sparql_query = data['sparql']
        results = execute_sparql_query(graph, sparql_query)
        
        # 3. 返回结果
        return jsonify({"results": results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)