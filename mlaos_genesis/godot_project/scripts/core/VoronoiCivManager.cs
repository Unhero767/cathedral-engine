using Godot;
using System.Collections.Generic;
using System.Runtime.InteropServices;

public partial class VoronoiCivManager : Node
{
    [StructLayout(LayoutKind.Sequential)]
    private struct SeedNode
    {
        public Vector2 Position;
        public float CulturalWeight; 
        public float AlignmentHash;  
    }

    private List<SeedNode> _activeCivilizations = new List<SeedNode>();
    private RenderingDevice _rd;
    private Rid _shader;
    private Rid _pipeline;

    public override void _Ready()
    {
        InitializeComputePipeline();
    }

    private void InitializeComputePipeline()
    {
        _rd = RenderingServer.CreateLocalRenderingDevice();
        RDShaderFile shaderFile = GD.Load<RDShaderFile>("res://assets/shaders/voronoi_compute.glsl");
        RDShaderSPIRV spirv = shaderFile.GetSpirV();
        _shader = _rd.ShaderCreateFromSpirV(spirv);
        _pipeline = _rd.ComputePipelineCreate(_shader);
        GD.Print("[Teal] Voronoi Compute Pipeline Initialized.");
    }

    public void RegisterSettlement(Vector2 coords, float initialWeight, float archiveHash)
    {
        _activeCivilizations.Add(new SeedNode 
        { 
            Position = coords, 
            CulturalWeight = initialWeight, 
            AlignmentHash = archiveHash 
        });
        GD.Print($"[Gold] Settlement Registered at {coords}. Cultural Weight: {initialWeight}");
        UpdateComputeShaderBuffers();
    }

    public void EvaluateBorderFriction(bool isCulturallyAligned, bool isGeographicallyContested)
    {
        BelnapDunnMatrix.TruthState borderState = BelnapDunnMatrix.EvaluateCollision(isCulturallyAligned, isGeographicallyContested);
        
        if (borderState == BelnapDunnMatrix.TruthState.Both)
        {
            GD.Print("[Bronze-Obsidian] Dialetheic Friction Detected. Border flagged as Contested Zone.");
        }
    }

    private void UpdateComputeShaderBuffers()
    {
        if (_activeCivilizations.Count == 0) return;

        int structSize = Marshal.SizeOf<SeedNode>();
        byte[] seedBytes = new byte[_activeCivilizations.Count * structSize];
        
        for (int i = 0; i < _activeCivilizations.Count; i++)
        {
            byte[] posBytesX = BitConverter.GetBytes(_activeCivilizations[i].Position.X);
            byte[] posBytesY = BitConverter.GetBytes(_activeCivilizations[i].Position.Y);
            byte[] weightBytes = BitConverter.GetBytes(_activeCivilizations[i].CulturalWeight);
            byte[] hashBytes = BitConverter.GetBytes(_activeCivilizations[i].AlignmentHash);
            
            int offset = i * structSize;
            System.Buffer.BlockCopy(posBytesX, 0, seedBytes, offset, 4);
            System.Buffer.BlockCopy(posBytesY, 0, seedBytes, offset + 4, 4);
            System.Buffer.BlockCopy(weightBytes, 0, seedBytes, offset + 8, 4);
            System.Buffer.BlockCopy(hashBytes, 0, seedBytes, offset + 12, 4);
        }
    }
}
