from flask import jsonify


def problem(status, title, detail, error_type=None):
    if error_type is None:
        error_type = "/errors/" + title.lower().replace(" ", "-")

    return jsonify({
        "type": error_type,
        "title": title,
        "status": status,
        "detail": detail
    }), status