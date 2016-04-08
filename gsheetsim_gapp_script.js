/*
 * POC Google Spreadsheet simulator POC script
 */

function sheetTestTest() {
  sheetTest('1w-chXNWK2GBaiSo7MCYv2-5YjDf1prb_Wa4zNlDQqs0', {interest_percent: 3.8, mortage: 50000});
}

function sheetTest(spreadsheet_id, inputs) {
  // copy the base sheet
  var ss = SpreadsheetApp.openById(spreadsheet_id).copy("Test" + Date.now());
  
  // get all the input keys from the "inputs" sheet
  var inputs_sheet = ss.getSheetByName("inputs");
  var inputs_range = inputs_sheet.getRange(2, 1, inputs_sheet.getLastRow() - 1); // ranges are 1 indexed
  var inputs_keys = inputs_range.getValues();
  
  // iterate through the passed inputs and set the values
  for (key in inputs) {
    var index = find_input(inputs_keys, key);
    if (index == -1) {
      Logger.log("Input key " + key + " not found in inputs sheet");
      break;
    }
    var value_range = inputs_sheet.getRange(index + 2, 2); // ranges are 1 indexed + skip header row
    value_range.setValue(inputs[key]);
  }
  
  // now get the outputs
  var outputs_sheet = ss.getSheetByName("outputs");
  var outputs_range = outputs_sheet.getRange(2, 1, outputs_sheet.getLastRow()-1, 2); // ranges are 1 indexed
  var outputs_values = outputs_range.getValues();
  
  var result = {};
  for (i = 0; i < outputs_values.length; i++) {
    var output = outputs_values[i];
    result[output[0]] = output[1];
  }
  return result;
}

/*
 * Helper function to find the input key. Returns the index or -1 if it's not found
 */

function find_input(input_keys, key) {
  for (i = 0; i < input_keys.length; i++) {
    if (input_keys[i][0] == key) {
      return i;
    }
  }
  return -1;
}