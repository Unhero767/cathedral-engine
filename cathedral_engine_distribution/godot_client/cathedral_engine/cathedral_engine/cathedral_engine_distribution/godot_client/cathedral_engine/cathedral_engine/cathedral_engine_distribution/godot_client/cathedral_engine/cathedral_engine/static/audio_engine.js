/**
 * Cathedral-Engine Generative Audio & Procedural Sound FX System
 * Synthesizes continuous 43.7 Hz carrier drone and real-time Web Audio sound effects.
 */

class CathedralAudioEngine {
    constructor() {
        this.ctx = null;
        this.carrierFreq = 43.7;
        this.droneGain = null;
        this.droneOsc1 = null;
        this.droneOsc2 = null;
        this.droneFilter = null;
        this.isMuted = true;
        this.activeSpectrum = "Gold";
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
            this.setupDrone();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    setupDrone() {
        // Master Drone Gain
        this.droneGain = this.ctx.createGain();
        this.droneGain.gain.setValueAtTime(0.0, this.ctx.currentTime);

        // Lowpass Filter for warm acoustic resonance
        this.droneFilter = this.ctx.createBiquadFilter();
        this.droneFilter.type = "lowpass";
        this.droneFilter.frequency.setValueAtTime(160, this.ctx.currentTime);

        // Fundamental Carrier Oscillator (43.7 Hz)
        this.droneOsc1 = this.ctx.createOscillator();
        this.droneOsc1.type = "sine";
        this.droneOsc1.frequency.setValueAtTime(this.carrierFreq, this.ctx.currentTime);

        // Harmonic Octave Oscillator (87.4 Hz with slight detune)
        this.droneOsc2 = this.ctx.createOscillator();
        this.droneOsc2.type = "triangle";
        this.droneOsc2.frequency.setValueAtTime(this.carrierFreq * 2 + 0.3, this.ctx.currentTime);

        this.droneOsc1.connect(this.droneFilter);
        this.droneOsc2.connect(this.droneFilter);
        this.droneFilter.connect(this.droneGain);
        this.droneGain.connect(this.ctx.destination);

        this.droneOsc1.start();
        this.droneOsc2.start();
    }

    toggleMute() {
        this.init();
        this.isMuted = !this.isMuted;
        const targetGain = this.isMuted ? 0.0 : 0.15;
        this.droneGain.gain.setTargetAtTime(targetGain, this.ctx.currentTime, 0.5);
        return !this.isMuted;
    }

    setSpectrum(spectrum) {
        this.activeSpectrum = spectrum;
        if (!this.droneFilter) return;
        
        // Modulate filter and harmonics according to 7-chromas
        let cutoff = 160;
        if (spectrum === "Gold") cutoff = 220;
        else if (spectrum === "Crimson") cutoff = 340;
        else if (spectrum === "Sapphire") cutoff = 180;
        else if (spectrum === "Obsidian") cutoff = 90;
        else if (spectrum === "Teal") cutoff = 260;

        this.droneFilter.frequency.setTargetAtTime(cutoff, this.ctx.currentTime, 1.0);
    }

    playDiceRoll() {
        if (this.isMuted || !this.ctx) return;
        for (let i = 0; i < 4; i++) {
            setTimeout(() => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = "square";
                osc.frequency.setValueAtTime(400 + Math.random() * 600, this.ctx.currentTime);
                gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.05);
            }, i * 45);
        }
    }

    playAttackHit(spectrum = "Gold") {
        if (this.isMuted || !this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "triangle";
        
        let freq = 120;
        if (spectrum === "Crimson") freq = 90;
        else if (spectrum === "Obsidian") freq = 60;
        else if (spectrum === "Cyan") freq = 240;

        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(30, this.ctx.currentTime + 0.15);

        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.18);
    }

    playCriticalHit() {
        if (this.isMuted || !this.ctx) return;
        const notes = [261.63, 329.63, 392.00, 523.25]; // C Major Chord
        notes.forEach((freq, idx) => {
            setTimeout(() => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
                gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.35);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.35);
            }, idx * 60);
        });
    }

    playVoidDrain() {
        if (this.isMuted || !this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(180, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(40, this.ctx.currentTime + 0.4);

        gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.4);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.4);
    }

    playParadoxBreak() {
        if (this.isMuted || !this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(300, this.ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(30, this.ctx.currentTime + 0.8);

        gain.gain.setValueAtTime(0.4, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.85);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.85);
    }
}

window.cathedralAudio = new CathedralAudioEngine();
