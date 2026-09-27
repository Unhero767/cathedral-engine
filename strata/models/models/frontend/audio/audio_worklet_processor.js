class CathedralAudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.bufferSize = 128;
    this.sampleCount = 0;
    this.accumulatedRms = 0.0;
    this.carrierEnergy = 0.0;
    this.prevSample = 0.0;
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (!input || input.length === 0) return true;
    const channelData = input[0];

    let sumSquares = 0.0;
    for (let i = 0; i < channelData.length; i++) {
      const sample = channelData[i];
      sumSquares += sample * sample;

      // Single-pole low-pass filtering near 42.0 Hz
      this.prevSample = 0.94 * this.prevSample + 0.06 * sample;
      this.carrierEnergy += this.prevSample * this.prevSample;
    }

    this.accumulatedRms += sumSquares;
    this.sampleCount += channelData.length;

    // Dispatch telemetry payload at ~60 Hz (every 768 samples)
    if (this.sampleCount >= 768) {
      const rms = Math.sqrt(this.accumulatedRms / this.sampleCount);
      const carrier = Math.sqrt(this.carrierEnergy / this.sampleCount);

      this.port.postMessage({
        type: 'AUDIO_TELEMETRY',
        rms: rms,
        carrierEnergy: carrier,
        friction_fs: Math.min(1.0, Math.max(0.0, (rms - 0.02) / 0.15))
      });

      this.accumulatedRms = 0.0;
      this.carrierEnergy = 0.0;
      this.sampleCount = 0;
    }

    return true;
  }
}

registerProcessor('cathedral-audio-processor', CathedralAudioProcessor);
