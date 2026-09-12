import React, { useState, useEffect, useRef } from 'react';

// ==========================================
// CHROMA CODEX: CORE SIMULATION ENGINE (v11.0)
// ==========================================

// Element Types & Metaphysical Constants
type ElementType = 'SILVER' | 'MERCURY' | 'LEAD' | 'BRONZE';
type TerrainType = 'HOLY_GROUND' | 'MUD' | 'FALLOUT' | 'GLASS_MATRIX';

interface PlayerState {
  health: number;          // 0 - 100
  maxHealth: number;
  breath: number;          // Void Lung Breath Pool (Mana)
  maxBreath: number;
  traumaIntake: number;    // Raw T entering system
  resonance: number;       // Resonance R = (ω_soul - ω_env) / Stress
  dampingRatio: number;    // ζ (0.0 = Fluid [Silver/Mercury], 1.0 = Static [Lead/Bronze])
  activePhase: ElementType;
  secondaryPhase: ElementType;
  currentTerrain: TerrainType;
}

export default function ChromaCodexSimulation() {
  // Engine State
  const [player, setPlayer] = useState<PlayerState>({
    health: 100,
    maxHealth: 100,
    breath: 50,
    maxBreath: 100,
    traumaIntake: 12.0,      // Baseline incoming stress
    resonance: 0.65,         // Initial resonance within target LRM [0.55 - 0.75]
    dampingRatio: 0.2,       // Default fluid state (Silver)
    activePhase: 'SILVER',
    secondaryPhase: 'LEAD',
    currentTerrain: 'HOLY_GROUND'
  });

  const [simulationLog, setSimulationLog] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState<boolean>(true);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Constants for Re-Weaving Equation R(T) = k*T - k'*T^2
  const K_COEFF = 4.5;
  const K_PRIME = 0.15;
  // Optimal Trauma Target: T_opt = k / (2*k') = 4.5 / 0.3 = 15.0
  const T_OPT = K_COEFF / (2 * K_PRIME);

  // Log Helper
  const logMessage = (msg: string) => {
    setSimulationLog(prev => [msg, ...prev.slice(0, 7)]);
  };

  // Phase Switch Handler (Law of Friction & Damping Modulation)
  const switchPhase = (primary: ElementType, secondary: ElementType) => {
    let targetDamping = 0.2;
    if (primary === 'LEAD' || primary === 'BRONZE') {
      targetDamping = 0.95; // High static damping (Load-bearing sanctuary)
    } else {
      targetDamping = 0.05; // Low fluid damping (Resonance amplification)
    }

    setPlayer(prev => ({
      ...prev,
      activePhase: primary,
      secondaryPhase: secondary,
      dampingRatio: targetDamping
    }));

    logMessage(`[PHASE CHANGE]: Shifted to ${primary}/${secondary} | Damping Ratio (ζ): ${targetDamping}`);
  };

  // Choir Gland Terrain Overwrite
  const castTerrain = (terrain: TerrainType) => {
    const cost = 25;
    if (player.breath < cost) {
      logMessage(`[OVERBREATHE WARNING]: Insufficient Breath to overwrite Lattice!`);
      return;
    }

    setPlayer(prev => ({
      ...prev,
      breath: prev.breath - cost,
      currentTerrain: terrain
    }));

    logMessage(`[CHOIR GLAND]: Lattice overwritten with texture -> ${terrain}`);
  };

  // Main Simulation Tick Loop (React useEffect Interval)
  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      setPlayer(prev => {
        // 1. Calculate Re-Weaving Resource Production R(T)
        // R(T) = k * T - k' * T^2
        const T = prev.traumaIntake;
        const generatedBreath = (K_COEFF * T) - (K_PRIME * Math.pow(T, 2));

        // 2. Adjust breath and health based on damping and optimal delta
        let newBreath = prev.breath + (generatedBreath * 0.1);
        let newHealth = prev.health;

        // Penalty if trauma deviates too far from T_opt (Overbreathe or Stagnation)
        const traumaDelta = Math.abs(T - T_OPT);
        if (T === 0) {
          newHealth -= 0.5; // Grey Stagnation penalty
        } else if (T > T_OPT * 1.5) {
          newHealth -= (traumaDelta * 0.2); // Overbreathe thermal damage
          logMessage(`[METALOGICAL BURN]: Trauma intake exceeds T_opt. Shunting to somatic sink...`);
        }

        // Clamp values
        newBreath = Math.max(0, Math.min(prev.maxBreath, newBreath));
        newHealth = Math.max(0, Math.min(prev.maxHealth, newHealth));

        // 3. Modulate Resonance based on Damping Ratio ζ
        // Low damping allows massive resonance peaks; high damping stabilizes against drift
        const stabilityDrift = (prev.dampingRatio > 0.5) ? 0.01 : (Math.random() * 0.04 - 0.02);
        let newResonance = Math.max(0.1, Math.min(1.0, prev.resonance + stabilityDrift));

        return {
          ...prev,
          breath: newBreath,
          health: newHealth,
          resonance: newResonance
        };
      });
    }, 500);

    return () => clearInterval(interval);
  }, [isRunning]);

  // Canvas Voxel Lattice Visualizer Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let angle = 0;

    const renderLattice = () => {
      angle += 0.02;
      ctx.fillStyle = '#0a0a0f'; // Vantablack Lattice Background
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Render Dynamic Terrain Grid based on player.currentTerrain
      const cols = 16;
      const rows = 12;
      const cellWidth = canvas.width / cols;
      const cellHeight = canvas.height / rows;

      for (let x = 0; x < cols; x++) {
        for (let y = 0; y < rows; y++) {
          const posX = x * cellWidth;
          const posY = y * cellHeight;

          // Color based on active terrain constant
          let strokeColor = '#222633';
          let fillColor = '#10131c';

          if (player.currentTerrain === 'HOLY_GROUND') {
            strokeColor = '#d4af3744'; // Gold Constant
            fillColor = (x + y) % 2 === 0 ? '#d4af3711' : '#10131c';
          } else if (player.currentTerrain === 'MUD') {
            strokeColor = '#4a5d4e55'; // Earth/Water
            fillColor = '#1d241e';
          } else if (player.currentTerrain === 'FALLOUT') {
            strokeColor = '#ff334466'; // Red Rupture Constant
            fillColor = '#241012';
          } else if (player.currentTerrain === 'GLASS_MATRIX') {
            strokeColor = '#00ffff55'; // Teal Recursive Crystal
            fillColor = '#0f2424';
          }

          ctx.strokeStyle = strokeColor;
          ctx.fillStyle = fillColor;
          ctx.lineWidth = 1;
          ctx.fillRect(posX + 2, posY + 2, cellWidth - 4, cellHeight - 4);
          ctx.strokeRect(posX + 2, posY + 2, cellWidth - 4, cellHeight - 4);
        }
      }

      // Render Central Heart-Oculus Pulse Wave
      ctx.beginPath();
      ctx.arc(canvas.width / 2, canvas.height / 2, 40 + Math.sin(angle * 3) * 8, 0, Math.PI * 2);
      ctx.strokeStyle = player.dampingRatio > 0.5 ? '#94a3b8' : '#38bdf8'; // Lead vs Silver tint
      ctx.lineWidth = 3;
      ctx.stroke();

      animationFrameId = requestAnimationFrame(renderLattice);
    };

    renderLattice();

    return () => cancelAnimationFrame(animationFrameId);
  }, [player.currentTerrain, player.dampingRatio]);

  return (
    <div style={{ backgroundColor: '#090a0f', color: '#e2e8f0', padding: '24px', fontFamily: 'monospace', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '20px', borderBottom: '1px solid #1e293b', width: '100%', maxWidth: '900px', paddingBottom: '12px' }}>
        <h1 style={{ margin: 0, fontSize: '22px', color: '#38bdf8', letterSpacing: '2px' }}>CHROMA CODEX | BIO-METAPHYSICAL ENGINE</h1>
        <p style={{ margin: '4px 0 0 0', fontSize: '12px', color: '#64748b' }}>MLAOS-Prime Runtime v11.0 | Phase Change & Re-Weaving Simulation</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', width: '100%', maxWidth: '900px' }}>
        
        {/* Left Column: Telemetry & Controls */}
        <div style={{ backgroundColor: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          
          <h3 style={{ margin: 0, fontSize: '14px', color: '#cbd5e1', borderBottom: '1px solid #374151', paddingBottom: '6px' }}>SOULFRAME TELEMETRY</h3>
          
          {/* Health & Breath Meters */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
              <span>Somatic Integrity (Health):</span>
              <span style={{ color: player.health < 30 ? '#ef4444' : '#22c55e' }}>{player.health.toFixed(1)} / {player.maxHealth}</span>
            </div>
            <div style={{ width: '100%', backgroundColor: '#1f2937', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${(player.health / player.maxHealth) * 100}%`, backgroundColor: player.health < 30 ? '#ef4444' : '#22c55e', height: '100%', transition: 'width 0.3s' }} />
            </div>
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
              <span>Void Lung Breath (Mana):</span>
              <span style={{ color: '#38bdf8' }}>{player.breath.toFixed(1)} / {player.maxBreath}</span>
            </div>
            <div style={{ width: '100%', backgroundColor: '#1f2937', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${(player.breath / player.maxBreath) * 100}%`, backgroundColor: '#38bdf8', height: '100%', transition: 'width 0.3s' }} />
            </div>
          </div>

          {/* Mathematical Engine Parameters */}
          <div style={{ backgroundColor: '#0f172a', padding: '10px', borderRadius: '6px', fontSize: '12px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div><strong>Trauma Intake ($T$):</strong> {player.traumaIntake.toFixed(1)} (Optimal: {T_OPT.toFixed(1)})</div>
            <div><strong>System Damping ($\zeta$):</strong> {player.dampingRatio.toFixed(2)} ({player.dampingRatio > 0.5 ? 'Static / Shielded' : 'Fluid / Agile'})</div>
            <div><strong>Resonance ($R$):</strong> {player.resonance.toFixed(3)} {player.resonance >= 0.55 && player.resonance <= 0.75 ? '🟢 (Gold Zone)' : '🟡 (Drift)'}</div>
          </div>

          {/* Phase Change Controls */}
          <h3 style={{ margin: '6px 0 0 0', fontSize: '14px', color: '#cbd5e1', borderBottom: '1px solid #374151', paddingBottom: '6px' }}>PHASE CHANGE ENGINE (Friction)</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            <button 
              onClick={() => switchPhase('SILVER', 'LEAD')}
              style={{ backgroundColor: player.activePhase === 'SILVER' ? '#0284c7' : '#1f2937', color: '#fff', border: 'none', padding: '8px', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold' }}>
              Silver / Lead (Balanced)
            </button>
            <button 
              onClick={() => switchPhase('MERCURY', 'BRONZE')}
              style={{ backgroundColor: player.activePhase === 'MERCURY' ? '#0d9488' : '#1f2937', color: '#fff', border: 'none', padding: '8px', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold' }}>
              Mercury / Bronze (Resonant)
            </button>
          </div>

          {/* Choir Gland Terrain Overwrite */}
          <h3 style={{ margin: '6px 0 0 0', fontSize: '14px', color: '#cbd5e1', borderBottom: '1px solid #374151', paddingBottom: '6px' }}>CHOIR GLAND OVERWRITE</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            <button onClick={() => castTerrain('HOLY_GROUND')} style={{ backgroundColor: '#334155', color: '#e2e8f0', border: '1px solid #475569', padding: '6px', borderRadius: '4px', cursor: 'pointer', fontSize: '10px' }}>
              Cast: Holy Ground
            </button>
            <button onClick={() => castTerrain('MUD')} style={{ backgroundColor: '#334155', color: '#e2e8f0', border: '1px solid #475569', padding: '6px', borderRadius: '4px', cursor: 'pointer', fontSize: '10px' }}>
              Cast: Mud
            </button>
            <button onClick={() => castTerrain('FALLOUT')} style={{ backgroundColor: '#334155', color: '#e2e8f0', border: '1px solid #475569', padding: '6px', borderRadius: '4px', cursor: 'pointer', fontSize: '10px' }}>
              Cast: Fallout Zone
            </button>
            <button onClick={() => castTerrain('GLASS_MATRIX')} style={{ backgroundColor: '#334155', color: '#e2e8f0', border: '1px solid #475569', padding: '6px', borderRadius: '4px', cursor: 'pointer', fontSize: '10px' }}>
              Cast: Glass Matrix
            </button>
          </div>

        </div>

        {/* Right Column: Voxel Lattice Visualizer & Terminal Log */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          
          <div style={{ backgroundColor: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '12px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', color: '#64748b', marginBottom: '8px' }}>LATTICE TEXTURE VISUALIZER: [{player.currentTerrain}]</span>
            <canvas ref={canvasRef} width={400} height={220} style={{ borderRadius: '4px', border: '1px solid #334155' }} />
          </div>

          <div style={{ backgroundColor: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '12px', flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '11px', color: '#64748b', marginBottom: '6px' }}>AUTOPOIETIC HEART TERMINAL LOG</span>
            <div style={{ backgroundColor: '#050508', border: '1px solid #1e293b', borderRadius: '4px', padding: '8px', height: '110px', overflowY: 'auto', fontSize: '11px', color: '#38bdf8', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {simulationLog.map((log, index) => (
                <div key={index} style={{ borderBottom: '1px dashed #1e293b', paddingBottom: '2px' }}>{log}</div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}