from flask import Flask, request, jsonify
from flask_cors import CORS
from rdflib import Graph
from rdflib.plugins.sparql import processUpdate
import json
from sparql_queries import InvolvedParty

app = Flask(__name__)

CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:3000"}})


@app.route('/query', methods=['POST'])
def handle_query():
    # 校验请求数据格式
    data = request.get_json()
    if not data or 'jsonld' not in data:
        return jsonify({"error": "Missing 'jsonld' in request body"}), 400
    query_actions = {
        "shipper_info": InvolvedParty.SHIPPERNAME,
        "consignee_info": InvolvedParty.CONSIGNEENAME
    }
    response = {}
    processor = JsonldProcessor(data['jsonld'])
    # try:
    #     由processor进行查询
    #     results = processor.execute_sparql_query( InvolvedParty.SHIPPERNAME )#ShipperName托运人信息
    #     result2 = processor.execute_sparql_query( InvolvedParty.CONSIGNEENAME )#ConsigneeName收货人信息
    #     # 3. 返回结果
    #     return jsonify({"results": results})
    # except Exception as e:
    #     print(e)
    #     return jsonify({"error": str(e)}), 400
    for key, query in query_actions.items():
        try:
            result = processor.execute_sparql_query(query)
            response[key] = result
        except Exception as e:
            response[f"{key}_error"] = str(e)
    
    return jsonify(response)

class JsonldProcessor:
    def __init__(self, jsonld_data):
        self.jsonld_data = jsonld_data
        self.graph = Graph()
        self.graph.parse(data=json.dumps(jsonld_data), format='json-ld')
    
    def jsonld_to_rdf_graph(self):
        """将 JSON-LD 数据转换为 RDF 图"""
        return self.graph
    def execute_sparql_query(self,sparql_query):
        """执行 SPARQL 查询并返回 JSON 序列化结果"""
        results = self.graph.query(sparql_query)
        # print(results)
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




if __name__ == '__main__':
    app.run(debug=True)