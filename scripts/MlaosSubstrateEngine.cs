using System;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using Godot;
using CathedralEngine.Core.Topological;
using CathedralEngine.Core.Paraconsistent;

namespace CathedralEngine.Core.Substrate
{
    public enum SubstrateElement : byte
    {
        Void = 0,
        Basalt = 1,      // Delta (Δ): Rigid stone masonry
        Sand = 2,        // Theta (Θ): Granular gravity
        Fluid = 3,       // Psi (Ψ): Hydrodynamic flow
        Lava = 4,        // Phi (Φ): High-thermal melting
        Acid = 5,        // Omega (Ω): Caustic dissolution
        HarmonicScar = 6 // Permineralized load-bearing ashlar
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct SubstrateCell
    {
        public SubstrateElement Element;
        public byte SpectralConstant;
        public ushort ThermalHeat;
        public float PrincipalStress;
    }

    [GlobalClass]
    public unsafe partial class MlaosSubstrateEngine : Node
    {
        [Export] public int GridWidth { get; set; } = 256;
        [Export] public int GridHeight { get; set; } = 256;
        [Export] public double TargetSimulationFrequency { get; set; } = 30.0;
        [Export] public float SomaticHeartbeatHz { get; set; } = 1.50f;

        [Export] public NodePath? LaplacianSolverPath { get; set; }
        [Export] public NodePath? MasterDissipatorPath { get; set; }

        private DiscreteLaplacianSolver? _laplacianSolver;
        private GkslMasterDissipator? _dissipator;

        private SubstrateCell* _currentBuffer;
        private SubstrateCell* _nextBuffer;
        private int _totalCells;
        private double _accumulatedTime = 0.0;
        private double _fixedTimeStep;
        private double _somaticPhase = 0.0;

        public event Action<int, double>? OnSimulationTickCompleted;

        public override void _Ready()
        {
            _fixedTimeStep = 1.0 / TargetSimulationFrequency;
            _totalCells = GridWidth * GridHeight;

            nuint bufferSizeBytes = (nuint)(_totalCells * sizeof(SubstrateCell));
            _currentBuffer = (SubstrateCell*)NativeMemory.AllocZeroed(bufferSizeBytes);
            _nextBuffer = (SubstrateCell*)NativeMemory.AllocZeroed(bufferSizeBytes);

            if (LaplacianSolverPath != null)
                _laplacianSolver = GetNodeOrNull<DiscreteLaplacianSolver>(LaplacianSolverPath);
            if (MasterDissipatorPath != null)
                _dissipator = GetNodeOrNull<GkslMasterDissipator>(MasterDissipatorPath);

            GD.Print($"[MlaosSubstrateEngine]: Initialized unmanaged double-buffer ({GridWidth}x{GridHeight} @ {TargetSimulationFrequency} Hz).");
        }

        public override void _Process(double delta)
        {
            _accumulatedTime += delta;
            _somaticPhase += delta * SomaticHeartbeatHz * Mathf.Tau;

            while (_accumulatedTime >= _fixedTimeStep)
            {
                ExecuteSubstrateTick();
                _accumulatedTime -= _fixedTimeStep;
            }
        }

        private void ExecuteSubstrateTick()
        {
            float somaticFactor = 1.0f + 0.15f * Mathf.Sin((float)_somaticPhase);

            for (int y = 0; y < GridHeight; y++)
            {
                for (int x = 0; x < GridWidth; x++)
                {
                    int index = y * GridWidth + x;
                    SubstrateCell cell = _currentBuffer[index];

                    if (cell.Element == SubstrateElement.Void)
                    {
                        _nextBuffer[index] = cell;
                        continue;
                    }

                    switch (cell.Element)
                    {
                        case SubstrateElement.Sand:
                            SimulateGranularGravity(x, y, index, cell);
                            break;

                        case SubstrateElement.Fluid:
                            SimulateFluidDynamics(x, y, index, cell);
                            break;

                        case SubstrateElement.Lava:
                            SimulateThermalAdvection(x, y, index, cell, somaticFactor);
                            break;

                        case SubstrateElement.Acid:
                            SimulateAcidDissolution(x, y, index, cell);
                            break;

                        case SubstrateElement.Basalt:
                        case SubstrateElement.HarmonicScar:
                            _nextBuffer[index] = cell;
                            break;

                        default:
                            _nextBuffer[index] = cell;
                            break;
                    }
                }
            }

            SubstrateCell* temp = _currentBuffer;
            _currentBuffer = _nextBuffer;
            _nextBuffer = temp;

            OnSimulationTickCompleted?.Invoke(_totalCells, _fixedTimeStep);
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private void SimulateGranularGravity(int x, int y, int index, SubstrateCell cell)
        {
            if (y < GridHeight - 1)
            {
                int below = (y + 1) * GridWidth + x;
                if (_currentBuffer[below].Element == SubstrateElement.Void || _currentBuffer[below].Element == SubstrateElement.Fluid)
                {
                    _nextBuffer[below] = cell;
                    _nextBuffer[index] = _currentBuffer[below];
                    return;
                }

                int belowLeft = (y + 1) * GridWidth + (x - 1);
                int belowRight = (y + 1) * GridWidth + (x + 1);

                if (x > 0 && _currentBuffer[belowLeft].Element == SubstrateElement.Void)
                {
                    _nextBuffer[belowLeft] = cell;
                    _nextBuffer[index] = default;
                    return;
                }
                if (x < GridWidth - 1 && _currentBuffer[belowRight].Element == SubstrateElement.Void)
                {
                    _nextBuffer[belowRight] = cell;
                    _nextBuffer[index] = default;
                    return;
                }
            }
            _nextBuffer[index] = cell;
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private void SimulateFluidDynamics(int x, int y, int index, SubstrateCell cell)
        {
            if (y < GridHeight - 1 && _currentBuffer[(y + 1) * GridWidth + x].Element == SubstrateElement.Void)
            {
                _nextBuffer[(y + 1) * GridWidth + x] = cell;
                _nextBuffer[index] = default;
                return;
            }

            int left = y * GridWidth + (x - 1);
            int right = y * GridWidth + (x + 1);

            if (x > 0 && _currentBuffer[left].Element == SubstrateElement.Void)
            {
                _nextBuffer[left] = cell;
                _nextBuffer[index] = default;
                return;
            }
            if (x < GridWidth - 1 && _currentBuffer[right].Element == SubstrateElement.Void)
            {
                _nextBuffer[right] = cell;
                _nextBuffer[index] = default;
                return;
            }

            _nextBuffer[index] = cell;
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private void SimulateThermalAdvection(int x, int y, int index, SubstrateCell cell, float somaticFactor)
        {
            if (y < GridHeight - 1)
            {
                int below = (y + 1) * GridWidth + x;
                if (_currentBuffer[below].Element == SubstrateElement.Sand)
                {
                    _nextBuffer[below] = new SubstrateCell
                    {
                        Element = SubstrateElement.Basalt,
                        SpectralConstant = 3,
                        ThermalHeat = (ushort)(cell.ThermalHeat * 0.75f * somaticFactor),
                        PrincipalStress = 45.2f
                    };
                }
            }
            _nextBuffer[index] = cell;
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private void SimulateAcidDissolution(int x, int y, int index, SubstrateCell cell)
        {
            if (y < GridHeight - 1)
            {
                int below = (y + 1) * GridWidth + x;
                if (_currentBuffer[below].Element != SubstrateElement.Void && _currentBuffer[below].Element != SubstrateElement.HarmonicScar)
                {
                    _nextBuffer[below] = default; // Dissolve into void
                    _nextBuffer[index] = default;
                    return;
                }
            }
            _nextBuffer[index] = cell;
        }

        public void InscribeBrush(int centerX, int centerY, int radius, SubstrateElement element)
        {
            for (int dy = -radius; dy <= radius; dy++)
            {
                int py = centerY + dy;
                if (py < 0 || py >= GridHeight) continue;

                for (int dx = -radius; dx <= radius; dx++)
                {
                    int px = centerX + dx;
                    if (px < 0 || px >= GridWidth) continue;

                    if (dx * dx + dy * dy <= radius * radius)
                    {
                        int idx = py * GridWidth + px;
                        _currentBuffer[idx] = new SubstrateCell
                        {
                            Element = element,
                            SpectralConstant = 1,
                            ThermalHeat = (ushort)(element == SubstrateElement.Lava ? 60000 : 0),
                            PrincipalStress = (element == SubstrateElement.Basalt || element == SubstrateElement.HarmonicScar) ? 45.2f : 0.0f
                        };
                    }
                }
            }
        }

        public void CopyBufferToRgba(byte[] rgba)
        {
            int pixelIndex = 0;
            for (int i = 0; i < _totalCells; i++)
            {
                SubstrateElement elem = _currentBuffer[i].Element;
                switch (elem)
                {
                    case SubstrateElement.Void:
                        rgba[pixelIndex] = 10; rgba[pixelIndex + 1] = 10; rgba[pixelIndex + 2] = 15; rgba[pixelIndex + 3] = 255;
                        break;
                    case SubstrateElement.Basalt:
                        rgba[pixelIndex] = 43; rgba[pixelIndex + 1] = 45; rgba[pixelIndex + 2] = 66; rgba[pixelIndex + 3] = 255;
                        break;
                    case SubstrateElement.Sand:
                        rgba[pixelIndex] = 200; rgba[pixelIndex + 1] = 162; rgba[pixelIndex + 2] = 75; rgba[pixelIndex + 3] = 255;
                        break;
                    case SubstrateElement.Fluid:
                        rgba[pixelIndex] = 0; rgba[pixelIndex + 1] = 229; rgba[pixelIndex + 2] = 255; rgba[pixelIndex + 3] = 255;
                        break;
                    case SubstrateElement.Lava:
                        rgba[pixelIndex] = 255; rgba[pixelIndex + 1] = 32; rgba[pixelIndex + 2] = 78; rgba[pixelIndex + 3] = 255;
                        break;
                    case SubstrateElement.Acid:
                        rgba[pixelIndex] = 164; rgba[pixelIndex + 1] = 121; rgba[pixelIndex + 2] = 226; rgba[pixelIndex + 3] = 255;
                        break;
                    case SubstrateElement.HarmonicScar:
                        rgba[pixelIndex] = 224; rgba[pixelIndex + 1] = 225; rgba[pixelIndex + 2] = 221; rgba[pixelIndex + 3] = 255;
                        break;
                }
                pixelIndex += 4;
            }
        }

        public void ClearGrid()
        {
            nuint bufferSizeBytes = (nuint)(_totalCells * sizeof(SubstrateCell));
            NativeMemory.Clear(_currentBuffer, bufferSizeBytes);
            NativeMemory.Clear(_nextBuffer, bufferSizeBytes);
        }

        public override void _ExitTree()
        {
            if (_currentBuffer != null) NativeMemory.Free(_currentBuffer);
            if (_nextBuffer != null) NativeMemory.Free(_nextBuffer);
        }
    }
}
