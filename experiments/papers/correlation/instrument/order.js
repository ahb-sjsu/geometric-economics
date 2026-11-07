// One participant's trial order, exactly as stimuli.py's presentation(seed) gives it (PILOT.md, "Participants and
// instrument"): numpy's SeedSequence of [SEED, 4, seed], its PCG64 generator (XSL-RR output), and
// Generator.permutation's Fisher-Yates shuffle, which draws with random_interval. instrument_roundtrip.py checks this
// against stimuli.py for thousands of seeds, in both modes.
"use strict";

const ORDER = (() => {
  const INIT_A = 0x43b0d7e5, MULT_A = 0x931e8875, INIT_B = 0x8b51f9dd, MULT_B = 0x58f38ded;
  const MIX_MULT_L = 0xca01f9dd, MIX_MULT_R = 0x4973f715;
  const M64 = (1n << 64n) - 1n, M128 = (1n << 128n) - 1n;
  const MULT = (2549297995355413924n << 64n) + 4865540595714422341n;      // PCG's default 128-bit multiplier

  function hashmix(value, hc) {
    value = (value ^ hc.v) >>> 0;
    hc.v = Math.imul(hc.v, MULT_A) >>> 0;
    value = Math.imul(value, hc.v) >>> 0;
    return (value ^ (value >>> 16)) >>> 0;
  }

  function mix(x, y) {
    const r = (Math.imul(MIX_MULT_L, x) - Math.imul(MIX_MULT_R, y)) >>> 0;
    return (r ^ (r >>> 16)) >>> 0;
  }

  // SeedSequence(entropy).generate_state(4, uint64), for entropy words below 2**32 (stimuli.SEED, 4, and a seed
  // below 2**31 each make one word).
  function seedState(entropy) {
    const pool = [0, 0, 0, 0], hc = {v: INIT_A};
    for (let i = 0; i < 4; i++) pool[i] = hashmix(i < entropy.length ? entropy[i] : 0, hc);
    for (let s = 0; s < 4; s++)
      for (let d = 0; d < 4; d++) if (s !== d) pool[d] = mix(pool[d], hashmix(pool[s], hc));
    for (let s = 4; s < entropy.length; s++)
      for (let d = 0; d < 4; d++) pool[d] = mix(pool[d], hashmix(entropy[s], hc));
    let h = INIT_B;
    const words = [];
    for (let i = 0; i < 8; i++) {
      let v = (pool[i % 4] ^ h) >>> 0;
      h = Math.imul(h, MULT_B) >>> 0;
      v = Math.imul(v, h) >>> 0;
      words.push((v ^ (v >>> 16)) >>> 0);
    }
    // the uint32 words viewed as little-endian uint64s
    return [0, 1, 2, 3].map(k => BigInt(words[2 * k]) | (BigInt(words[2 * k + 1]) << 32n));
  }

  function pcg64(entropy) {
    const v = seedState(entropy);
    const initstate = (v[0] << 64n) | v[1], initseq = (v[2] << 64n) | v[3];
    const inc = ((initseq << 1n) | 1n) & M128;
    let state = 0n, buffered = null;
    const step = () => { state = (state * MULT + inc) & M128; };
    step();
    state = (state + initstate) & M128;
    step();
    function next64() {
      step();
      const x = ((state >> 64n) ^ state) & M64, rot = state >> 122n;
      return ((x >> rot) | (x << ((64n - rot) & 63n))) & M64;
    }
    function next32() {                    // numpy hands out each 64-bit draw as two 32-bit halves, low first
      if (buffered !== null) {
        const b = buffered;
        buffered = null;
        return b;
      }
      const n = next64();
      buffered = Number(n >> 32n);
      return Number(n & 0xffffffffn);
    }
    function interval(max) {                // numpy's random_interval: masked rejection, 32-bit draws below 2**32
      if (max === 0) return 0;
      let mask = max;
      mask |= mask >>> 1; mask |= mask >>> 2; mask |= mask >>> 4; mask |= mask >>> 8; mask |= mask >>> 16;
      let value;
      while ((value = (next32() & mask) >>> 0) > max);
      return value;
    }
    return {next64, interval};
  }

  function permute(rng, ids) {
    const a = ids.slice();
    for (let i = a.length - 1; i >= 1; i--) {
      const j = rng.interval(i);
      const t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  // presentation(seed): block R, then the rest of the main set, then (pilot only) the pilot-only trials, each part
  // shuffled with one generator in that order. An empty part draws nothing, as in stimuli.py.
  function presentation(seed, parts) {
    const rng = pcg64([STIMULI.seed, 4, seed]);
    return [].concat(...parts.map(p => (p.length ? permute(rng, p) : [])));
  }

  return {presentation, pcg64};
})();
