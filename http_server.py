from flask import Flask, request, jsonify
from flask_cors import CORS

from paddle_ner.server import server
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["DEBUG"] = False
CORS(app)


@app.route("/parse", methods=["GET"])
def single_tokenizer():
    message = request.args.get("q")
    print(message)

    span_info = server(message)

    span_set = SpanSet([Span(i[0], i[1], i[2]) for i in span_info])

    response = {
        "text": "".join(message),
        "spans": [{"start": i.start, "end": i.end, "type": i.entity} for i in span_set],
        "ents": list({i.entity.lower() for i in span_set}),
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
