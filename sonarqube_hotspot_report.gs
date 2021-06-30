function myFunction() {

  // variables
  var page_limit = 500;
  var p = 1;
  var uname = "username";
  var passwd = "password"
  var url = "https://your-sonarqube-url/api/hotspots/search?projectKey=<project-key>"
  
  // initialising Spreadsheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  Logger.log(sheet)

  var rows = [],
  data;

  // params for authentication
  var options = {};
  options.headers = {"Authorization": "Basic " + Utilities.base64Encode(uname + ":" + passwd)};

  var response = UrlFetchApp.fetch(url, options);
  var dataset = JSON.parse(response.getContentText());
  var total_issue = dataset.paging.total;
  Logger.log(total_issue);
  
  while(total_issue > 0){
    var response = UrlFetchApp.fetch(url + "&p="+ p + "&type=json", options);
    var dataset = JSON.parse(response.getContentText());
    var security_hotspots = dataset.hotspots;
    Logger.log(security_hotspots);
    for (i = 0; i < security_hotspots.length; i++) {
      data = security_hotspots[i];
      rows.push([data.key, data.component, data.project, data.securityCategory, data.vulnerabilityProbability, data.status, data.line, data.message, data.assignee, data.author, data.creationDate, data.updateDate]); // Entities in security hotspots
    }
    total_issue = total_issue - page_limit;
    p = p + 1;
  }
}