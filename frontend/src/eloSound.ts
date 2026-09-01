let audioContext: AudioContext | null = null;

function getAudioContext() {
  if (!audioContext) audioContext = new AudioContext();
  return audioContext;
}

export function playELOSound(kind: 'login' | 'click' | 'success' | 'close' = 'click') {
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
    gain.gain.exponentialRampToValueAtTime(0.045, now + 0.015);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + (notes.length > 1 ? 0.28 : 0.14));
    oscillator.connect(gain).connect(ctx.destination);
    oscillator.start(now);
    oscillator.stop(now + (notes.length > 1 ? 0.3 : 0.16));
  } catch {
    // Audio is optional and must never break authentication or navigation.
  }
}
