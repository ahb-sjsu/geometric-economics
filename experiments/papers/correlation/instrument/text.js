// Every word the participant reads, in one place, so that the review board and the owner can read and change the
// wording without touching task.js. `c` holds the session's values: the charity chosen and its short name, the
// number of trials, the minutes, the base payment, the cents per point, and the deployment's contact details and
// receipts address (config.js). The consent text is a draft for the ethics application (PILOT.md, "The open
// items", 3); the board's approved text replaces it.
"use strict";

const TEXT = {
  title: "Choices about points for you and for a charity",

  device: () => `
    <h1>Please use a larger window</h1>
    <p>This study shows two options side by side. It needs a window at least 1000 pixels wide and 620 pixels high,
    on a desktop or laptop computer.</p>
    <p>Please make this window larger, or maximize it. The study will continue by itself once the window is large
    enough.</p>`,

  no_id: () => `
    <h1>This link is missing your Prolific ID</h1>
    <p>Please open the study from its page on Prolific, so that the link carries your Prolific ID.</p>`,

  not_ready: () => `
    <h1>This study is not open yet</h1>
    <p>Please return the study on Prolific. Nothing has been recorded.</p>`,

  consent: c => `
    <h1>Consent to take part in a research study</h1>
    <p class="draft">${c.draft ? "DRAFT consent text for the ethics review. Not approved." : ""}</p>
    <p><b>Study:</b> ${TEXT.title}.<br>
    <b>Researcher:</b> ${c.contact.pi}, San José State University (${c.contact.email}).</p>
    <p><b>What you will do.</b> The study takes about ${c.minutes} minutes. You will choose a charity, read the
    rules, answer four questions about them, and then make ${c.n_trials} choices. Each choice is between two
    options, and each option gives points to you and points to the charity you chose.${c.mode === "pilot" ?
      " At the end you will answer four short questions about the study." : ""}</p>
    <p><b>Payment.</b> You will receive $${c.base} for taking part. One of your choices is drawn at random at the
    end and paid for real: up to $5.00 to you as a bonus, and up to $5.00 to the charity as a donation. If you do
    not answer the four questions about the rules correctly within two tries, the study ends there and you
    receive the $${c.base}.</p>
    <p><b>Risks and benefits.</b> The risks are no greater than those of everyday computer use. You may not
    benefit directly, apart from the payment.</p>
    <p><b>Your data.</b> We record your Prolific ID, the charity you choose, your answers, your choices and how
    long each choice takes. We do not ask for your name or contact details. Before the data are analyzed, your
    Prolific ID is replaced by a code, and the file linking the two is kept private by the research team.</p>
    <p><b>Taking part is voluntary.</b> You may stop at any time by closing this page and returning the study on
    Prolific.</p>
    <p><b>Questions.</b> About the study: ${c.contact.email}. About your rights as a participant:
    ${c.contact.irb}. Protocol ${c.contact.protocol}.</p>
    <p>Do you agree to take part?</p>`,

  agree: "I agree, and I am 18 or older",
  decline: "I do not agree",

  declined: () => `
    <h1>Thank you</h1>
    <p>You chose not to take part, and nothing has been recorded. Please return the study on Prolific.</p>`,

  intro: c => `
    <h1>How the study works</h1>
    <p>You will make ${c.n_trials} choices. Each one is between two options: Option A on the left and Option B on
    the right.</p>
    <p>Each option gives points to <b>you</b> and points to <b>a charity</b>. On each, points run from 0 to 100,
    and 100 is the most. A bar shows the points: an empty bar is 0 and a full bar is 100.</p>
    <p>At the end, the computer draws one of your choices at random and pays it for real.</p>
    <ul>
      <li>Your points from that choice are paid to you as a bonus on Prolific, at ${c.cents} cents a point.</li>
      <li>The charity's points from that choice are donated to the charity, at ${c.cents} cents a point.</li>
    </ul>
    <p>So the paid choice can be worth up to $5.00 to you and up to $5.00 to the charity. Any of your choices may be
    the one that is paid, so treat each one as if it counts.</p>
    <p>First, you will choose the charity.</p>`,

  charity_head: () => `
    <h1>Choose your charity</h1>
    <p>The charity you choose receives the donation from the paid choice. It is the charity in every choice you
    make.</p>`,

  charities: {
    "American Red Cross": "disaster relief and blood services in the United States",
    "Doctors Without Borders USA": "emergency medical care around the world",
    "Feeding America": "food for people facing hunger in the United States",
    "St. Jude Children's Research Hospital": "treatment and research for children with cancer and other diseases",
    "World Wildlife Fund": "protecting wildlife and nature",
  },

  rules: c => `
    <h1>Two kinds of option</h1>
    <p><b>A sure option</b> gives fixed points. In this example you get 70 points and ${c.short} gets 55.</p>
    <div class="example">${c.example_sure}</div>
    <p><b>A coin-flip option</b> has two outcomes, Heads and Tails, each with a 1 in 2 chance. If a coin-flip option
    is the paid choice, the computer flips a fair coin, and you and the charity get the outcome it lands on. In
    this example, Heads gives you 90 points and ${c.short} 30; Tails gives you 60 points and ${c.short} 30.</p>
    <div class="example">${c.example_coin}</div>
    <p>If this coin-flip option were paid and the coin landed Tails, you would get 60 points, a bonus of $3.00,
    and ${c.charity} would get 30 points, a donation of $1.50.</p>
    <p>There are no right or wrong answers. Choose the option you prefer.</p>
    <p>The research team makes the donations after the study, one payment to each charity, and publishes the
    receipts at ${c.receipts_url}.</p>
    <p>Next come four questions about these rules.</p>`,

  quiz_head: c => `
    <h1>Four questions about the rules</h1>
    <p>${c.attempt === 1 ? "Please answer all four." : "Second try. Please answer all four again."}</p>`,

  // The correct answer of each question is `key`, counted from 0.
  quiz: c => [
    {q: "On the choice that is paid, what happens to the points you get?",
     options: [`They are paid to me as a bonus, at ${c.cents} cents a point.`, "Nothing. They are only a score.",
               "They are donated to the charity.", "They are paid only if I finish quickly."], key: 0},
    {q: "On the choice that is paid, what happens to the charity's points?",
     options: ["They are paid to me.", `They are donated to ${c.charity}, at ${c.cents} cents a point.`,
               "Nothing. They are only a score.", "They are donated only if most of my choices favor the charity."],
     key: 1},
    {q: "A coin-flip option is the paid choice. How is its outcome decided?",
     options: ["I get the average of its two outcomes.", "I get the better of its two outcomes.",
               "A fair coin is flipped, and I get the outcome it lands on.", "I get both outcomes."], key: 2},
    {q: "How many of your choices are paid?",
     options: ["All of them, added up.", "The last one.", "The one I took longest over.",
               "One, drawn at random at the end."], key: 3},
  ],

  quiz_retry: c => `
    <h1>Not all of your answers were right</h1>
    <p>Here are the rules again. You have one more try.</p>
    <ul>
      <li>One of your ${c.n_trials} choices is drawn at random at the end, and only that one is paid.</li>
      <li>Your points from it are paid to you as a bonus, at ${c.cents} cents a point.</li>
      <li>The charity's points from it are donated to ${c.charity}, at ${c.cents} cents a point.</li>
      <li>If it is a coin-flip option, a fair coin decides which of its two outcomes is paid.</li>
    </ul>`,

  quiz_failed: c => `
    <h1>Thank you</h1>
    <p>The answers were not all right on the second try, so the study ends here. You will receive the payment of
    $${c.base} for taking part.</p>`,

  ready: c => `
    <h1>The choices</h1>
    <p>You answered all four questions correctly. The ${c.n_trials} choices start now.</p>
    <p>Click <b>Choose A</b> or <b>Choose B</b> for the option you prefer. Any choice may be the one that is paid.
    Please stay on this page until you finish; the study saves your progress as you go.</p>`,

  reminder: "Any choice may be the one that is paid.",

  debrief_head: () => `
    <h1>Four last questions</h1>`,

  debrief: c => ({
    belief: {q: `How sure are you that the donation to ${c.charity} will really be made?`,
             low: "Not at all sure", high: "Completely sure"},
    rule: {q: "Which of your choices will be paid?",
           options: ["All of them, added up.", "One, drawn at random.", "The last one.", "None of them."], key: 1},
    difficulty: {q: "How hard were the choices?", low: "Very easy", high: "Very hard"},
    strategy: {q: "In a sentence or two, how did you make your choices? (optional)"},
  }),

  payment: c => `
    <h1>Your paid choice</h1>
    <p>The computer drew choice ${c.pos} of ${c.n_trials}. In it you chose Option ${c.letter}:</p>
    <div class="example">${c.card}</div>
    ${c.coin ? `<p>The coin landed <b>${c.coin}</b>.</p>` : ""}
    <p>You get ${c.self_points} points: a bonus of <b>$${c.bonus}</b>, paid on Prolific after the study.<br>
    ${c.charity} gets ${c.charity_points} points: a donation of <b>$${c.donation}</b>.</p>`,

  saving: "Saving your answers…",
  saved: "Your answers are saved. Click Finish to return to Prolific.",
  save_failed: "Your answers could not be saved yet. Please check your connection and click Try again. If it " +
               "keeps failing, click Finish anyway and send the researcher a message on Prolific.",
  finish: "Finish and return to Prolific",
  finish_anyway: "Finish anyway",
  retry: "Try again",

  done: () => `
    <h1>You have finished</h1>
    <p>Thank you for taking part. If Prolific did not open, please use the button below.</p>`,

  continue: "Continue",
  start: "Start the choices",
  submit: "Submit",
};
