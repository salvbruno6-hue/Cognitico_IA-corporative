let audioContext: AudioContext | null = null;
let ambientMaster: GainNode | null = null;
let ambientOscillators: OscillatorNode[] = [];
let ambientLfo: OscillatorNode | null = null;
let ambientLfoGain: GainNode | null = null;
let soundEnabled = true;
let soundVolume = 0.7;

function getAudioContext() {
  if (!audioContext) audioContext = new AudioContext();
  return audioContext;
}

export function setELOSoundEnabled(enabled: boolean) {
  soundEnabled = enabled;
  if (!enabled) stopELOAmbient();
}

export function setELOSoundVolume(volume: number) {
  soundVolume = Math.max(0, Math.min(1, volume));
  if (ambientMaster && audioContext) {
    ambientMaster.gain.setTargetAtTime(soundVolume * 0.035, audioContext.currentTime, 0.8);
  }
}

/**
 * Starts the ELO ambient "aura" using Web Audio synthesis.
 * No external audio file is required and no audio leaves the browser.
 * Browsers require a user gesture before audio can be unlocked, so the
 * login button intentionally calls this before starting OAuth navigation.
 */
export function startELOAmbient() {
  if (!soundEnabled || soundVolume <= 0 || ambientMaster) return;

  try {
    const ctx = getAudioContext();
    if (ctx.state === 'suspended') void ctx.resume();

    const master = ctx.createGain();
    master.gain.setValueAtTime(0.0001, ctx.currentTime);
    master.gain.exponentialRampToValueAtTime(Math.max(0.001, soundVolume * 0.035), ctx.currentTime + 1.8);
    master.connect(ctx.destination);
    ambientMaster = master;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(900, ctx.currentTime);
    filter.Q.setValueAtTime(0.5, ctx.currentTime);
    filter.connect(master);

    const frequencies = [98, 146.83, 196];
    ambientOscillators = frequencies.map((frequency, index) => {
      const oscillator = ctx.createOscillator();
      const gain = ctx.createGain();
      oscillator.type = index === 0 ? 'sine' : 'triangle';
      oscillator.frequency.setValueAtTime(frequency, ctx.currentTime);
      oscillator.detune.setValueAtTime(index * 4 - 4, ctx.currentTime);
      gain.gain.setValueAtTime(index === 0 ? 0.45 : 0.18, ctx.currentTime);
      oscillator.connect(gain).connect(filter);
      oscillator.start();
      return oscillator;
    });

    // Very slow modulation creates a breathing/emanating quality without a rhythmic pulse.
    const lfo = ctx.createOscillator();
    const lfoGain = ctx.createGain();
    lfo.type = 'sine';
    lfo.frequency.setValueAtTime(0.075, ctx.currentTime);
    lfoGain.gain.setValueAtTime(0.012, ctx.currentTime);
    lfo.connect(lfoGain).connect(master.gain);
    lfo.start();
    ambientLfo = lfo;
    ambientLfoGain = lfoGain;

    localStorage.setItem('elo-audio-unlocked', '1');
  } catch {
    // Audio is optional and must never break authentication or navigation.
  }
}

export function stopELOAmbient() {
  if (!audioContext || !ambientMaster) return;
  try {
    const now = audioContext.currentTime;
    ambientMaster.gain.cancelScheduledValues(now);
    ambientMaster.gain.setTargetAtTime(0.0001, now, 0.35);
    window.setTimeout(() => {
      ambientOscillators.forEach((oscillator) => { try { oscillator.stop(); } catch { /* already stopped */ } });
      try { ambientLfo?.stop(); } catch { /* already stopped */ }
      ambientOscillators = [];
      ambientLfo = null;
      ambientLfoGain = null;
      ambientMaster?.disconnect();
      ambientMaster = null;
    }, 1200);
  } catch {
    ambientMaster = null;
  }
}

export function playELOSound(kind: 'login' | 'click' | 'success' | 'close' = 'click') {
  if (!soundEnabled || soundVolume <= 0) return;
  try {
    const ctx = getAudioContext();
    if (ctx.state === 'suspended') void ctx.resume();
    const now = ctx.currentTime;
    const oscillator = ctx.createOscillator();
    const gain = ctx.createGain();
    const frequencies = {
      login: [392, 523.25],
      click: [440],
      success: [523.25, 659.25, 783.99],
      close: [330],
    } as const;
    const notes = frequencies[kind];
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(notes[0], now);
    if (notes.length > 1) oscillator.frequency.setValueAtTime(notes[1], now + 0.08);
    if (notes.length > 2) oscillator.frequency.setValueAtTime(notes[2], now + 0.16);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.045 * soundVolume, now + 0.015);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + (notes.length > 1 ? 0.28 : 0.14));
    oscillator.connect(gain).connect(ctx.destination);
    oscillator.start(now);
    oscillator.stop(now + (notes.length > 1 ? 0.3 : 0.16));
  } catch {
    // Audio is optional and must never break authentication or navigation.
  }
}
