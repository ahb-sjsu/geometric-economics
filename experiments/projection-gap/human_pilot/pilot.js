/* Dear Ethicist — projection-gap human pilot (self-contained).
 *
 * Between-subjects design: each subject is assigned ONE pole (lo/hi) per contrast,
 * a random reframing, randomized order, with attention checks. Records
 * {contrast, pole, choice, rt, ...} in the SAME schema analyze_human.py expects.
 * Data is offered as a JSONL download and (optionally) POSTed to a Google Apps
 * Script / Sheets endpoint. No dependencies, no PII beyond coarse demographics.
 */
const CONFIG = {
  // Paste a Google Apps Script Web App URL to log to Sheets; leave "" for download-only.
  SHEETS_ENDPOINT: "",
  PROLIFIC_PARAM: "PROLIFIC_PID",   // ?PROLIFIC_PID=... appended by Prolific
};

const stage = document.getElementById("stage");
const bar = document.getElementById("bar");
const S = { subject: uuid(), started: Date.now(), demo: {}, records: [], letters: null, queue: [], i: 0 };

function uuid() { return "s-" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4); }
function rnd(a) { return a[Math.floor(Math.random() * a.length)]; }
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = (Math.random() * (i + 1)) | 0; [a[i], a[j]] = [a[j], a[i]]; } return a; }
function qparam(k) { return new URLSearchParams(location.search).get(k) || ""; }

async function boot() {
  S.letters = await (await fetch("letters.json")).json();
  S.prolific = qparam(CONFIG.PROLIFIC_PARAM);
  consent();
}

function consent() {
  stage.innerHTML = `
    <div class="subject">Consent</div>
    <p>This is a research study about how people give advice on everyday decisions. You will read
       short letters and choose the advice you would give. Participation is voluntary and anonymous;
       you may stop at any time. Some responses may be used to determine a small bonus.</p>
    <p class="muted">No identifying information is collected beyond your Prolific ID (for payment) and
       coarse demographics. By continuing you consent to participate.</p>
    <button class="go" id="c">I consent — begin</button>`;
  document.getElementById("c").onclick = demographics;
}

function demographics() {
  stage.innerHTML = `
    <div class="subject">A few quick questions</div>
    <div class="row">
      <div><label>Age</label><input id="age" type="number" min="18" max="99"></div>
      <div><label>Gender</label><select id="gender">
        <option value="">—</option><option>Female</option><option>Male</option>
        <option>Non-binary</option><option>Prefer not to say</option></select></div>
    </div>
    <label>How comfortable are you with numbers and probabilities?</label>
    <select id="num"><option value="">—</option><option>Not at all</option><option>Somewhat</option>
      <option>Very</option></select>
    <p></p><button class="go" id="d">Start the letters</button>`;
  document.getElementById("d").onclick = () => {
    S.demo = { age: val("age"), gender: val("gender"), numeracy: val("num") };
    buildQueue(); next();
  };
}
function val(id){ return document.getElementById(id).value; }

function buildQueue() {
  // between-subjects: assign one pole per contrast at the subject level
  const items = [];
  for (const c of S.letters.contrasts) {
    const pole = Math.random() < 0.5 ? "lo" : "hi";
    const text = rnd(c.poles[pole].reframings);
    items.push({ kind: "contrast", id: c.id, pole, text, subject: c.subject,
                 optionA: c.optionA, optionB: c.optionB, meta: c });
  }
  shuffle(items);
  // insert an attention check about 60% through
  const at = S.letters.attention_checks[0];
  items.splice(Math.floor(items.length * 0.6), 0,
    { kind: "attn", id: at.id, text: at.body, subject: at.subject,
      optionA: at.optionA, optionB: at.optionB, correct: at.correct });
  S.queue = items;
}

function next() {
  if (S.i >= S.queue.length) return finish();
  bar.style.width = (100 * S.i / S.queue.length) + "%";
  const it = S.queue[S.i];
  const t0 = performance.now();
  stage.innerHTML = `
    <div class="subject">${it.subject}</div>
    <div class="body">${it.text}</div>
    <div class="opts">
      <button class="opt" data-c="A">${it.optionA}</button>
      <button class="opt" data-c="B">${it.optionB}</button>
    </div>`;
  stage.querySelectorAll("button.opt").forEach(b => b.onclick = () => {
    const choice = b.getAttribute("data-c");
    const rt = Math.round(performance.now() - t0);
    if (it.kind === "attn") {
      S.records.push({ subject: S.subject, contrast: it.id, kind: "attn", choice,
                       attn_pass: choice === it.correct, rt });
    } else {
      S.records.push({ subject: S.subject, model: "human", contrast: it.id, pole: it.pole,
                       kind: it.meta.kind, family: it.meta.family, domain: it.meta.domain,
                       coord: it.meta.coord, sign_pred: it.meta.sign_pred, choice, rt });
    }
    S.i++; next();
  });
}

function finish() {
  bar.style.width = "100%";
  const payload = {
    subject: S.subject, prolific: S.prolific || null, demo: S.demo,
    ms: Date.now() - S.started, records: S.records,
  };
  // JSONL: one row per record (analyze_human.py reads these directly)
  const jsonl = S.records.map(r => JSON.stringify({ ...r, prolific: S.prolific || null })).join("\n");
  if (CONFIG.SHEETS_ENDPOINT) {
    fetch(CONFIG.SHEETS_ENDPOINT, { method: "POST", body: JSON.stringify(payload) }).catch(() => {});
  }
  const blob = new URL(URL.createObjectURL(new Blob([jsonl], { type: "application/x-ndjson" })));
  stage.innerHTML = `
    <div class="subject">Thank you</div>
    <p>You're done. Your responses were recorded.</p>
    <p class="muted">If the researcher asked you to submit a file, download it below.</p>
    <p><a class="go" style="text-decoration:none" href="${blob}" download="dearethicist_${S.subject}.jsonl">Download my responses</a></p>
    <details><summary class="muted">show raw</summary><textarea readonly>${jsonl}</textarea></details>`;
}

boot();
