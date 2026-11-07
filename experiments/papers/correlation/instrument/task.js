// The instrument (PILOT.md, "Participants and instrument"; DESIGN.md, "Stimuli and procedure"): one participant's
// session in the browser. Consent, the charity, the rules and the quiz (two tries), the trials in the order
// stimuli.py's presentation(seed) gives (order.js), the pilot's debrief, the paid trial, and the return to Prolific.
//
// The whole session record is saved at checkpoints through DataPipe's API (README.md), each save a new file named
// <Prolific ID>_<session>_<n>.json, so a session that stops early still leaves its last checkpoint. Nothing is
// saved before consent. The record is also kept in the browser, so a reload resumes the same session: the same
// order, the choices already made, the same paid trial. export_pilot.py turns the saved files into the export that
// split_pilot.py reads.
"use strict";

const PARAMS = {
  cents: 5,                          // per point, self and charity alike (PILOT.md, "The open items", 5)
  base: {pilot: "8.40", main: "7.00"},
  minutes: {pilot: 42, main: 35},
  main_trials: 140,                  // t_main_end is stamped when the 140th choice is made
  quiz_tries: 2,
  checkpoint_every: 20,              // choices between saves during the trials
  blank_ms: 300,                     // the empty screen between two trials
  min_width: 1000,
  min_height: 620,
  short: {"American Red Cross": "Red Cross", "Doctors Without Borders USA": "Doctors Without Borders",
          "Feeding America": "Feeding America", "St. Jude Children's Research Hospital": "St. Jude",
          "World Wildlife Fund": "World Wildlife Fund"},
};
const RECORD_FORMAT = "correlation-session/1";
// the stages a participant can leave the page in, which a reload resumes and leaving warns about
const ACTIVE = ["intro", "charity", "rules", "quiz", "quiz_retry", "ready", "trials", "debrief"];
const Q = new URLSearchParams(location.search);
let S = null;                        // the session record
let BUILD = null;                    // MANIFEST.json's build hash, if the page could read it

// ---- small helpers ---------------------------------------------------------------------------------------------

const now = () => Date.now() / 1000;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const money = cents => (cents / 100).toFixed(2);
const app = () => document.getElementById("app");

function esc(s) {
  return String(s).replace(/[&<>"']/g, ch => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[ch]));
}

function randomWord() {
  const u = new Uint32Array(1);
  crypto.getRandomValues(u);
  return u[0];
}

function randomInt(n) {              // uniform on 0..n-1, by rejection
  const limit = Math.floor(2 ** 32 / n) * n;
  let u;
  do { u = randomWord(); } while (u >= limit);
  return u % n;
}

function hex(bytes) {
  const b = new Uint8Array(bytes);
  crypto.getRandomValues(b);
  return Array.from(b, x => x.toString(16).padStart(2, "0")).join("");
}

function page(html) {
  app().innerHTML = html;
  window.scrollTo(0, 0);
}

function onClick(id, fn) {
  document.getElementById(id).addEventListener("click", fn);
}

function ctx(extra) {
  const charity = S && S.charity;
  return Object.assign({
    mode: CONFIG.mode, n_trials: STIMULI.parts[CONFIG.mode].reduce((n, p) => n + p.length, 0),
    minutes: PARAMS.minutes[CONFIG.mode], base: PARAMS.base[CONFIG.mode], cents: PARAMS.cents,
    charity: charity ? esc(charity) : "", short: charity ? esc(PARAMS.short[charity]) : "",
    receipts_url: esc(CONFIG.receipts_url), draft: CONFIG.consent_draft,
    contact: Object.fromEntries(Object.entries(CONFIG.contact).map(([k, v]) => [k, esc(v)])),
  }, extra || {});
}

function configured() {
  const c = CONFIG;
  return ["pilot", "main"].includes(c.mode) && c.datapipe_url && c.experiment_id && c.completion_url &&
    c.completion.finished && c.completion.quiz_failed && c.receipts_url &&
    ["pi", "email", "irb", "protocol"].every(k => c.contact[k]);
}

// ---- the record, in the browser and in storage -----------------------------------------------------------------

const key = pid => `correlation-${CONFIG.mode}-${pid}`;

function persist() {
  try { localStorage.setItem(key(S.platform_id), JSON.stringify(S)); } catch (e) { /* storage off: no resume */ }
}

function restore(pid) {
  try {
    const s = JSON.parse(localStorage.getItem(key(pid)));
    if (s && s.format === RECORD_FORMAT && s.mode === CONFIG.mode && s.stimuli_sha256 === STIMULI.sha256) return s;
  } catch (e) { /* none, or unreadable */ }
  return null;
}

function newSession(pid) {
  const seed = randomWord() >>> 1;   // below 2**31, as stimuli.presentation's seeds
  return {
    format: RECORD_FORMAT, build: BUILD, mode: CONFIG.mode, platform_id: pid,
    study_id: Q.get("STUDY_ID"), prolific_session: Q.get("SESSION_ID"), sid: hex(8),
    stimuli_sha256: STIMULI.sha256, display_sha256: STIMULI.display_sha256,
    order_seed: seed, order: ORDER.presentation(seed, STIMULI.parts[CONFIG.mode]),
    t_start: now(), t_main_end: null, t_end: null, stage: "intro", charity: null,
    quiz: {attempts: 0, passed: false, answers: []}, trials: [], debrief: null, payment: null, finished: false,
    seq: 0, reloads: 0, hidden: 0, save_errors: [], viewport: [window.innerWidth, window.innerHeight],
  };
}

let chain = Promise.resolve();

// Save the whole record as a new file. Saves go one at a time, in order. Resolves to {ok}.
function checkpoint(kind) {
  S.seq += 1;
  persist();
  const name = `${S.platform_id}_${S.sid}_${String(S.seq).padStart(3, "0")}.json`;
  const text = JSON.stringify(Object.assign({}, S, {kind, saved_utc: new Date().toISOString()}));
  const job = chain.then(() => deliver(name, text));
  chain = job.catch(() => null);
  return job;
}

// DataPipe's answers (README.md): 201 stored, 202 queued (stored later; not to be sent again), 400 with an error
// code. FILE_EXISTS means an earlier try of this same file arrived. Network failures and 5xx are tried again.
async function deliver(name, text) {
  let last = {ok: false, status: null, error: "network"};
  for (let k = 0; k < 6; k++) {
    if (k) await sleep(1000 * 2 ** (k - 1));
    try {
      const res = await fetch(CONFIG.datapipe_url, {
        method: "POST", headers: {"Content-Type": "application/json", Accept: "*/*"},
        body: JSON.stringify({experimentID: CONFIG.experiment_id, filename: name, data: text})});
      if (res.status === 201 || res.status === 202) return {ok: true};
      let error = null;
      try { error = (await res.json()).error || null; } catch (e) { /* no body */ }
      if (error === "FILE_EXISTS") return {ok: true};
      last = {ok: false, status: res.status, error};
      if (res.status < 500 && res.status !== 429) break;
    } catch (e) {
      last = {ok: false, status: null, error: "network"};
    }
  }
  S.save_errors.push({file: name, status: last.status, error: last.error, t: now()});
  persist();
  return last;
}

// ---- drawing options -------------------------------------------------------------------------------------------

function bars(o) {
  const m = 100 - o[1], c = 100 - o[2];
  const row = (who, cls, v) => `<div class="row"><span class="who">${who}</span><span class="track">` +
    `<span class="fill ${cls}" style="width:${v}%"></span></span><span class="num">${v}</span></div>`;
  return row("You", "self", m) + row(esc(PARAMS.short[S.charity]), "charity", c);
}

// One option: a sure outcome, or two at even odds, Heads first, as stimuli.py lists them. `side` adds the button;
// `realized` marks the outcome the coin gave.
function card(option, letter, opt) {
  const o = opt || {};
  const body = option.length === 2
    ? option.map((x, i) =>
        `<div class="outcome${o.realized === i ? " realized" : ""}"><div class="face">${i ? "Tails" : "Heads"} ` +
        `<span class="chance">(1 in 2)</span></div>${bars(x)}</div>`).join("")
    : `<div class="outcome">${bars(option[0])}</div>`;
  const button = o.side === undefined ? "" :
    `<button class="choose" data-side="${o.side}" disabled>Choose ${letter}</button>`;
  return `<div class="option${o.chosen ? " chosen" : ""}"><div class="letter">Option ${letter}</div>` +
    `<div class="kind">${option.length === 2 ? "Coin flip" : "For sure"}</div><div class="body">${body}</div>${button}</div>`;
}

function actions(...buttons) {
  return `<div class="actions">${buttons.map(([id, label, cls, off]) =>
    `<button id="${id}"${cls ? ` class="${cls}"` : ""}${off ? " disabled" : ""}>${label}</button>`).join("")}</div>`;
}

// ---- the stages ------------------------------------------------------------------------------------------------

function go(stage) {
  S.stage = stage;
  persist();
  route();
}

function route() {
  ({intro, charity, rules, quiz, quiz_retry: quizRetry, ready, trials: showTrial, debrief, payment,
    quiz_failed: quizFailed, done}[S.stage] || done)();
}

function whenLargeEnough(fn) {
  const big = () => window.innerWidth >= PARAMS.min_width && window.innerHeight >= PARAMS.min_height;
  if (big()) return fn();
  page(TEXT.device());
  const check = () => {
    if (!big()) return;
    window.removeEventListener("resize", check);
    fn();
  };
  window.addEventListener("resize", check);
}

function consent(pid) {
  page(TEXT.consent(ctx()) + actions(["agree", TEXT.agree], ["decline", TEXT.decline, "secondary"]));
  onClick("agree", () => {
    S = newSession(pid);
    checkpoint("consent");
    go("intro");
  });
  onClick("decline", () => page(TEXT.declined()));
}

function intro() {
  page(TEXT.intro(ctx()) + actions(["next", TEXT.continue]));
  onClick("next", () => go("charity"));
}

function charity() {
  const list = Object.entries(TEXT.charities).map(([name, what], i) =>
    `<label><input type="radio" name="charity" value="${i}"> <b>${esc(name)}</b>: ${esc(what)}</label>`).join("");
  page(TEXT.charity_head() + `<div class="charity-list">${list}</div>` + actions(["next", TEXT.continue, "", true]));
  const names = Object.keys(TEXT.charities);
  document.querySelectorAll("input[name=charity]").forEach(r =>
    r.addEventListener("change", () => { document.getElementById("next").disabled = false; }));
  onClick("next", () => {
    const r = document.querySelector("input[name=charity]:checked");
    if (!r) return;
    S.charity = names[Number(r.value)];
    checkpoint("charity");
    go("rules");
  });
}

function rules() {
  page(TEXT.rules(ctx({example_sure: card([[1, 30, 45]], "A"),
                       example_coin: card([[0.5, 10, 70], [0.5, 40, 70]], "B")})) + actions(["next", TEXT.continue]));
  onClick("next", () => go("quiz"));
}

function radios(name, labels) {
  return labels.map((label, i) => `<label><input type="radio" name="${name}" value="${i}"> ${label}</label>`).join("");
}

function quiz() {
  const qs = TEXT.quiz(ctx());
  page(TEXT.quiz_head(ctx({attempt: S.quiz.attempts + 1})) +
       qs.map((q, i) => `<div class="q" data-q="${i}"><p><b>${i + 1}. ${q.q}</b></p>${radios(`q${i}`, q.options)}</div>`)
         .join("") + actions(["submit", TEXT.submit, "", true]));
  const answered = () => qs.map((_, i) => document.querySelector(`input[name=q${i}]:checked`));
  document.querySelectorAll(".q input").forEach(r => r.addEventListener("change", () => {
    document.getElementById("submit").disabled = answered().some(a => !a);
  }));
  onClick("submit", () => {
    const a = answered();
    if (a.some(x => !x)) return;
    const answers = a.map(x => Number(x.value));
    S.quiz.attempts += 1;
    S.quiz.answers.push(answers);
    if (answers.every((x, i) => x === qs[i].key)) {
      S.quiz.passed = true;
      checkpoint("quiz");
      go("ready");
    } else if (S.quiz.attempts < PARAMS.quiz_tries) {
      checkpoint("quiz");
      go("quiz_retry");
    } else {
      go("quiz_failed");
    }
  });
}

function quizRetry() {
  page(TEXT.quiz_retry(ctx()) + actions(["next", TEXT.retry]));
  onClick("next", () => go("quiz"));
}

function ready() {
  page(TEXT.ready(ctx()) + actions(["next", TEXT.start]));
  onClick("next", () => go("trials"));
}

// One trial. The buttons come on two frames after the options are drawn, and the response time runs from then to
// the click. A reload during a trial shows the same trial again, timed afresh.
function showTrial() {
  const k = S.trials.length;
  if (k >= S.order.length) return afterTrials();
  const id = S.order[k], opts = STIMULI.trials[String(id)];
  page(`<div class="progress"><span>Choice ${k + 1} of ${S.order.length}</span><span class="meter">` +
       `<span style="width:${(100 * k / S.order.length).toFixed(1)}%"></span></span></div>` +
       `<div class="pair" id="pair" data-trial-id="${id}" data-pos="${k}">` +
       `${card(opts[0], "A", {side: 0})}${card(opts[1], "B", {side: 1})}</div>` +
       `<p class="reminder">${TEXT.reminder}</p>`);
  const buttons = Array.from(document.querySelectorAll("button.choose"));
  let t0 = null, taken = false;
  requestAnimationFrame(() => requestAnimationFrame(() => {
    t0 = performance.now();
    buttons.forEach(b => { b.disabled = false; });
    document.getElementById("pair").dataset.live = "1";
  }));
  buttons.forEach(b => b.addEventListener("click", () => {
    if (t0 === null || taken) return;
    taken = true;
    const rt = Math.round(performance.now() - t0);
    buttons.forEach(x => { x.disabled = true; });
    choose(id, k, Number(b.dataset.side), rt);
  }));
}

function choose(id, pos, side, rt) {
  S.trials.push({id, pos, choice: side, rt_ms: rt});
  const n = S.trials.length;
  if (n === PARAMS.main_trials) S.t_main_end = now();
  persist();
  if (n % PARAMS.checkpoint_every === 0 || n === PARAMS.main_trials) checkpoint("trials");
  app().innerHTML = "";
  setTimeout(showTrial, PARAMS.blank_ms);
}

function afterTrials() {
  if (CONFIG.mode === "pilot") return go("debrief");
  S.finished = true;
  go("payment");
}

function debrief() {
  const d = TEXT.debrief(ctx());
  const scale = (name, item) => `<div class="q" data-q="${name}"><p><b>${item.q}</b></p><div class="scale">` +
    `<span>${item.low}</span>${[1, 2, 3, 4, 5].map(v =>
      `<label><input type="radio" name="${name}" value="${v}"> ${v}</label>`).join("")}<span>${item.high}</span></div></div>`;
  page(TEXT.debrief_head() + scale("belief", d.belief) +
       `<div class="q" data-q="rule"><p><b>${d.rule.q}</b></p>${radios("rule", d.rule.options)}</div>` +
       scale("difficulty", d.difficulty) +
       `<div class="q" data-q="strategy"><p><b>${d.strategy.q}</b></p>` +
       `<textarea name="strategy" rows="3" maxlength="2000"></textarea></div>` + actions(["submit", TEXT.submit, "", true]));
  const pick = name => document.querySelector(`input[name=${name}]:checked`);
  document.querySelectorAll(".q input").forEach(r => r.addEventListener("change", () => {
    document.getElementById("submit").disabled = !(pick("belief") && pick("rule") && pick("difficulty"));
  }));
  onClick("submit", () => {
    if (!(pick("belief") && pick("rule") && pick("difficulty"))) return;
    const rule = Number(pick("rule").value);
    S.debrief = {belief: Number(pick("belief").value), payment_rule_correct: rule === d.rule.key,
                 difficulty: Number(pick("difficulty").value),
                 strategy: document.querySelector("textarea[name=strategy]").value.trim(), rule_answer: rule};
    S.finished = true;
    go("payment");
  });
}

// The paid trial: one of the trials shown, drawn at random, and a fair coin if the option chosen in it is a coin
// flip. The draw is kept in the record before it is shown, so a reload shows the same one.
function draw() {
  const k = randomInt(S.trials.length), t = S.trials[k];
  const option = STIMULI.trials[String(t.id)][t.choice];
  const face = option.length === 2 ? randomInt(2) : null;
  const o = option[face === null ? 0 : face];
  const self = 100 - o[1], charityPoints = 100 - o[2];
  return {trial: t.id, pos: t.pos, choice: t.choice, coin: face === null ? null : ["heads", "tails"][face],
          self_points: self, charity_points: charityPoints, bonus_cents: self * PARAMS.cents,
          donation_cents: charityPoints * PARAMS.cents, bonus: self * PARAMS.cents / 100,
          donation: charityPoints * PARAMS.cents / 100};
}

function payment() {
  if (!S.payment) {
    S.payment = draw();
    S.t_end = now();
    persist();
  }
  const p = S.payment, letter = p.choice ? "B" : "A";
  const option = STIMULI.trials[String(p.trial)][p.choice];
  page(TEXT.payment(ctx({pos: p.pos + 1, letter, coin: p.coin === null ? null : (p.coin === "heads" ? "Heads" : "Tails"),
                         card: card(option, letter, {chosen: true, realized: p.coin === null ? undefined :
                                                                    (p.coin === "heads" ? 0 : 1)}),
                         self_points: p.self_points, charity_points: p.charity_points,
                         bonus: money(p.bonus_cents), donation: money(p.donation_cents)})) + finishBlock());
  finalSave("final", CONFIG.completion.finished);
}

function quizFailed() {
  page(TEXT.quiz_failed(ctx()) + finishBlock());
  finalSave("quiz_failed", CONFIG.completion.quiz_failed);
}

function finishBlock() {
  return `<p class="status" id="status"></p>` + actions(["finish", TEXT.finish, "", true],
                                                          ["retry", TEXT.retry, "secondary hidden"]);
}

// The last save must arrive before the participant is sent back to Prolific (Prolific's advice). If it keeps
// failing, they can try again, or finish anyway and write to the researcher.
async function finalSave(kind, code) {
  const status = document.getElementById("status"), fin = document.getElementById("finish");
  const retry = document.getElementById("retry");
  const leave = () => {
    S.stage = "done";
    persist();
    location.href = CONFIG.completion_url + encodeURIComponent(code);
  };
  fin.addEventListener("click", leave);
  retry.addEventListener("click", async () => {
    retry.classList.add("hidden");
    await attempt();
  });
  async function attempt() {
    status.textContent = TEXT.saving;
    fin.disabled = true;
    const r = await checkpoint(kind);
    if (r.ok) {
      status.textContent = TEXT.saved;
      fin.textContent = TEXT.finish;
    } else {
      status.textContent = TEXT.save_failed;
      fin.textContent = TEXT.finish_anyway;
      retry.classList.remove("hidden");
    }
    fin.disabled = false;
    document.body.dataset.saved = r.ok ? "1" : "0";
  }
  await attempt();
}

function done() {
  const code = S.finished ? CONFIG.completion.finished : CONFIG.completion.quiz_failed;
  page(TEXT.done() + actions(["finish", TEXT.finish]));
  onClick("finish", () => { location.href = CONFIG.completion_url + encodeURIComponent(code); });
}

// ---- start -----------------------------------------------------------------------------------------------------

document.addEventListener("visibilitychange", () => {
  if (document.hidden && S && S.stage === "trials") {
    S.hidden += 1;
    persist();
  }
});

window.addEventListener("beforeunload", e => {
  if (S && ACTIVE.includes(S.stage)) {
    e.preventDefault();
    e.returnValue = "";
  }
});

async function start() {
  document.title = TEXT.title;
  try {
    BUILD = (await (await fetch("MANIFEST.json", {cache: "no-store"})).json()).build || null;
  } catch (e) {
    BUILD = null;
  }
  const pid = Q.get("PROLIFIC_PID") || "";
  if (!/^[A-Za-z0-9_-]{1,64}$/.test(pid)) return page(TEXT.no_id());
  if (!configured()) return page(TEXT.not_ready());
  S = restore(pid);
  if (S) {
    S.reloads += 1;
    persist();
    return route();
  }
  whenLargeEnough(() => consent(pid));
}

start();
