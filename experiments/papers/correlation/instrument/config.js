// The deployment's settings (README.md, "Deploying"). They are filled in for each study on Prolific and are not
// part of the seal: none of them changes a trial, the order, the payment rule or the analysis. Until every field is
// filled the page records nothing and asks the participant to return the study. The round trip writes its own copy
// (instrument_roundtrip.py).
"use strict";

const CONFIG = {
  mode: "pilot",                                   // "pilot": 160 trials and the debrief; "main": 140 trials
  datapipe_url: "https://pipe.jspsych.org/api/data/",
  experiment_id: "",                               // the DataPipe experiment's id, from its dashboard
  completion_url: "https://app.prolific.com/submissions/complete?cc=",
  completion: {finished: "", quiz_failed: ""},     // the Prolific study's two completion codes
  receipts_url: "",                                // where the donation receipts will be published
  contact: {pi: "", email: "", irb: "", protocol: ""},
  consent_draft: true,                             // false once the review board's approved consent is in text.js
};
