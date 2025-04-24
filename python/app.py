from flask import Flask,request,jsonify
import sys,os,signal

# A  lot of the funtions in the extract data are still not made. We need to change these imports as the project moves on to make sure everything works. Pretty sure it should be fine rigth now
import middleware
import ai_service
import logging


logging.basicConfig(level=logging.DEBUG)

app = Flask(_name__)


@app.route("/health")
def health_check():
    return "OK",200

@app.route("/ask",methods = ['POST'])
def extract_data():
    app.logger.info("Start seemed to work")

    data = request.get_json()

    #Make sure that it is valid json
    valid,error = validate_request(data)
    if not valid:
        return jsonify({"error":error},400)

    #Format the input
    prompt = format_prompt(data['context'],data['question'],data.get('project_info'))     

    #Send to the openAI API
    ai_response  = send_to_openai(prompt)

    #Filter the output this is to make sure that perry never returns any code

    clean_response = filter_response(ai_response)

    # We need to format it as markdown so it can be displayed easier
    markdown_response = f"**Response:**\n\n{clean_response}"

    return jsonify(
        {
            "response": markdown_response,
            #Think that we might need to add more stuff here but i thibk response should be just fine
        }
    )


@app.route("/shutdown",methods = ['POST'])
def shutdown():
    app.logger.info("Shutdown worked")
    shutdown_server()
    return jsonify({"message" : "Server is shutting down..."})




if __name__ == '__main__':
    app.run(debug=True,port=5000)