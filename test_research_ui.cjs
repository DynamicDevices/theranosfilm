'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {httpUrl, makeProposal} = require('./research-ui.js');
const values = {id:'sample-record', claim:'A bounded source observation.', display_name:'Contributor',
  profile_url:'https://github.com/example', source_url:'https://example.org/source', locator:'paragraph 2',
  supports:'Only this limited observation.', kind:'primary_document', limitations:'Not an independent audit.',
  rights_note:'Original text; source linked only.', consent:true};
test('helper produces proposed JSON, not a review or acceptance', () => {
  const record = makeProposal({...values, status:'accepted', history:['forged']}, '2026-11-21T12:00:00Z');
  assert.equal(record.status, 'proposed'); assert.deepEqual(record.history, []);
  assert.equal(record.contributor.identity_status, 'self_reported');
});
test('unsafe source links and credential-bearing links are rejected', () => {
  for (const url of ['javascript:alert(1)', 'data:text/html,x', '//example.org', 'https://u:p@example.org', 'https://example.org/has space']) {
    assert.throws(() => httpUrl(url));
  }
});
test('rights consent and supported source types are required', () => {
  assert.throws(() => makeProposal({...values, consent:false}, '2026-11-21T12:00:00Z'));
  assert.throws(() => makeProposal({...values, kind:'verified_truth'}, '2026-11-21T12:00:00Z'));
});
test('untrusted text stays text and is not executed', () => {
  const record = makeProposal({...values, claim:'<img src=x onerror=alert(1)>'}, '2026-11-21T12:00:00Z');
  assert.equal(record.claim, '<img src=x onerror=alert(1)>');
});
