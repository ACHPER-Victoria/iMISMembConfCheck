import azure.functions as func
#import logging
from os import environ
import json
from iMISpy import openAPI

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

api = openAPI(environ)

@app.route(route="HttpTriggerWakeUp")
def HttpTriggerWakeUp(req: func.HttpRequest) -> func.HttpResponse:
    # preemptivly call the Query with dummy data to "Warm" up the query cache...
    api.apiIterator("query", [["QueryName", environ["Query"]], ["Email", "test@example.com"]])
    return func.HttpResponse("WakeUp Success.", status_code=200)

@app.route(route="HttpTriggerEOYConfMembCheck")
def HttpTriggerEOYConfMembCheck(req: func.HttpRequest) -> func.HttpResponse:
    try: email = req.get_json()["email"]
    except (ValueError, KeyError): return func.HttpResponse("Invalid data", status_code=400)
    data = {"iMIS ID": 0, "isMember": "N"}
    count = 0
    for x in api.apiIterator("query", [["QueryName", environ["Query"]], ["Email", email]]):
        data["iMIS ID"] = x["ID"]
        data["isMember"] = x["ValidMember"]
    return func.HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")