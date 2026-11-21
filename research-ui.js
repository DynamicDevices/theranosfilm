'use strict';
// Optional enhancements only. No source URLs are fetched; no data is submitted.
function httpUrl(value) {
  if (/\s|[\u0000-\u001f]/u.test(value)) throw new Error('Use an absolute HTTP(S) URL without spaces.');
  const url = new URL(value);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) {
    throw new Error('Use an HTTP(S) URL without a username or password.');
  }
  return value;
}

function makeProposal(values, createdAt) {
  if (!values.consent) throw new Error('Explicit rights and privacy consent is required.');
  const text = key => {
    const value = String(values[key] || '').trim();
    if (!value) throw new Error('Complete all required fields.');
    return value;
  };
  const id = text('id');
  if (!/^[a-z0-9][a-z0-9-]+$/.test(id)) throw new Error('Use a lowercase, hyphenated record ID.');
  const kinds = ['primary_document', 'legal_allegation', 'judicial_finding', 'reporting', 'patent', 'film', 'other'];
  if (!kinds.includes(values.kind)) throw new Error('Choose a source type.');
  const profile = httpUrl(text('profile_url'));
  if (!profile.startsWith('https://')) throw new Error('The public profile must use HTTPS.');
  const proposal = {
    id, claim: text('claim'),
    contributor: {display_name: text('display_name'), profile_url: profile, identity_status: 'self_reported'},
    submitted_at: createdAt,
    sources: [{url: httpUrl(text('source_url')), locator: text('locator'), supports: text('supports'), kind: values.kind, rights_note: text('rights_note')}],
    limitations: text('limitations'), status: 'proposed', license: 'CC-BY-SA-4.0', license_consent: true, history: []
  };
  if (values.supersedes && values.supersedes.trim()) {
    if (!/^[a-z0-9][a-z0-9-]+$/.test(values.supersedes.trim())) throw new Error('Use an existing record ID for a correction.');
    proposal.supersedes = values.supersedes.trim();
  }
  return proposal;
}

function initResearch() {
  const search = document.querySelector('#claim-search');
  if (search) {
    const category = document.querySelector('#claim-category');
    const cards = [...document.querySelectorAll('[data-claim]')];
    const update = () => {
      const query = search.value.trim().toLocaleLowerCase('en-GB');
      let visible = 0;
      for (const card of cards) {
        card.hidden = !((category.value === 'all' || card.dataset.category === category.value)
                       && card.textContent.toLocaleLowerCase('en-GB').includes(query));
        if (!card.hidden) visible += 1;
      }
      document.querySelector('#claim-count').textContent = `${visible} of ${cards.length} claims shown.`;
    };
    search.addEventListener('input', update);
    category.addEventListener('change', update);
    const revealHash = () => {
      let target;
      try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
      if (target && target.matches('[data-claim]') && target.hidden) {
        search.value = ''; category.value = 'all'; update(); target.scrollIntoView();
      }
    };
    window.addEventListener('hashchange', revealHash);
    update(); revealHash();
  }
  const form = document.querySelector('#contribution-form');
  if (form) {
    let downloadUrl;
    const context = new URLSearchParams(location.search).get('claim');
    if (context && /^[a-z0-9-]+$/.test(context)) {
      document.querySelector('#proposal-status').textContent = `You followed a correction link for ${context}. Identify that entry in your claim.`;
    }
    form.addEventListener('submit', event => {
      event.preventDefault();
      const status = document.querySelector('#proposal-status');
      const output = document.querySelector('#proposal-output');
      const download = document.querySelector('#proposal-download');
      output.value = ''; download.hidden = true;
      if (downloadUrl) { URL.revokeObjectURL(downloadUrl); downloadUrl = null; }
      try {
        if (!form.reportValidity()) return;
        const values = Object.fromEntries(new FormData(form));
        values.consent = form.elements.consent.checked;
        const record = makeProposal(values, new Date().toISOString());
        const json = JSON.stringify(record, null, 2);
        output.value = json;
        downloadUrl = URL.createObjectURL(new Blob([json + '\n'], {type: 'application/json'}));
        download.href = downloadUrl; download.download = `${record.id}.json`; download.hidden = false;
        status.textContent = 'JSON prepared locally. Nothing has been submitted or accepted. Inspect it, then use GitHub to propose the record.';
      } catch (error) { status.textContent = error.message; }
    });
  }
  document.querySelectorAll('[data-enhancement]').forEach(element => { element.hidden = false; });
}
if (typeof document !== 'undefined') initResearch();
if (typeof module !== 'undefined') module.exports = {httpUrl, makeProposal};
