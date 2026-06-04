// Duet CRM Data Sync v5 — Google Apps Script
// No chunking — data split across multiple keys instead
// Col A = data, Col B = timestamp, Col C = device name

var VALID_KEYS = ['leads_1','leads_2','leads_3','appointments','agents','pipeline_2025','pipeline_2026','periods_2025','periods_2026','settings'];

function doGet(e) {
  var action = e.parameter.action;

  if (action === 'loadAll') {
    var result = {};
    VALID_KEYS.forEach(function(key) {
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(key);
      if (sheet && sheet.getLastRow() >= 1) {
        var data = sheet.getRange(1, 1).getValue();
        var updated = sheet.getRange(1, 2).getValue();
        var device = sheet.getRange(1, 3).getValue();
        result[key] = { data: data || '', updated: updated || '', device: device || '' };
      } else {
        result[key] = { data: '', updated: '', device: '' };
      }
    });
    return ContentService.createTextOutput(JSON.stringify({ status: 'ok', data: result }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  if (action === 'save') {
    var key = e.parameter.key;
    if (VALID_KEYS.indexOf(key) === -1) {
      return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'Invalid key: ' + key }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    var data = e.parameter.data || '';
    var device = e.parameter.device || '';
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(key);
    var timestamp = new Date().toISOString();
    if (sheet) {
      sheet.getRange(1, 1).setValue(data);
      sheet.getRange(1, 2).setValue(timestamp);
      sheet.getRange(1, 3).setValue(device);
    }
    return ContentService.createTextOutput(JSON.stringify({ status: 'ok', key: key, updated: timestamp }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'Unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}
