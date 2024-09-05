from atlassian import Jira
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

def connectJIRA(jira_server, jira_username, jira_api_token, cloud=True):
    """
    Method to connect to the JIRA server
    """
    try:
        jira = Jira(url=jira_server, username=jira_username, password=jira_api_token, cloud=True)
        return jira
    except Exception as e:
        # print("Error occured during connecting to Jira, Exception is {}".format(e))
        return {"error": f"Error occurred during connecting to Jira: {e}"}

def writeToCSV(data_to_write, file_name):
    """
    Method to write data to a csv file
    """
    try:
        df = pd.DataFrame(data_to_write)
        df.to_csv(file_name, index=False)
        return {"message": f"Successfully written issues to {file_name}"}
    except Exception as e:
        return {"error": f"Error occurred during writing to file: {e}"}

@app.route('/fetch_issues', methods=['GET'])
def fetch_issues():
    data = request.get_json()
    assignee = data['assignee']
    days = data.get('days', 365)
    jira_username = data['jira_username']
    jira_api_token = data['jira_api_token']

    # JIRA configuration
    # Replace the value of the JIRA server based on your Organisation
    jira_server = 'https://org.atlassian.net/'

    output_file_name = assignee.split()[0] + "_completed_jira_details.csv"

    # Connect to JIRA
    jira = connectJIRA(jira_server, jira_username, jira_api_token, cloud=True)

    jql_query = f"assignee = '{assignee}' AND status = Done AND resolved >= -{days}d"
    # Add any fields which you want to fetch the details for.
    fields = ['summary','description','priority','reporter', 'customfield_10006', 'customfield_12396', 'comment']
    results = jira.jql(jql_query, fields)
    jira_issues = results["issues"]
    data_to_write = []
    for issue in jira_issues:
        # Checking if Quarter Custom Field is set
        if issue['fields']['customfield_12396'] is None:
            quarter = "Not Present"
        else:
            quarter = issue['fields']['customfield_12396']['value']
        # Checking if Sprint Custom Field is set
        if issue['fields']['customfield_10006'] is None:
            sprint_list = ["Not Present"]
        else:
            sprint_list = []
            sprints_len = len(issue['fields']['customfield_10006'])
            for i in range(sprints_len):
                sprint_list.append(issue['fields']['customfield_10006'][i]['name'])
        comments_body = []
        if 'comment' in issue['fields']:
            comments = issue['fields']['comment']['comments']
            for i in range(0, len(comments)):
                comments_body.append(comments[i]['body'])

        data_to_write.append({
            "ID": issue['key'],
            "Summary": issue['fields']['summary'],
            "Description": issue['fields']['description'],
            "Reporter": issue['fields']['reporter']['displayName'],
            "Comment": comments_body,
            "Quarter" : quarter,
            "Priority": issue['fields']['priority']['name'],
            "Number of Sprints": sprint_list,
        })
    # Write to CSV file
    writeToCSV(data_to_write, output_file_name)
    return jsonify(data_to_write)

if __name__ == '__main__':
    app.run(debug=True)
