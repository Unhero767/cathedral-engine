using Godot;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Master Technical Specification Ledger for the Cathedral-Engine.
    /// Codifies the absolute operational parameters, schema versions, and runtime axioms.
    /// </summary>
    public static class CathedralEngineMasterSpecification
    {
        public const string EngineName = "Cathedral-Engine";
        public const string RuntimeVersion = "v0.4-DualTopology";
        public const int SchemaVersion = 2;
        public const int FormatVersion = 1;
        public const string CoordinateSpace = "CANONICAL_NORMALIZED";
        public const int ScarRecordSize = 88;
        public const int HeaderSize = 136;

        public static void PrintSpecification()
        {
            System.Console.WriteLine("================================================================================");
            System.Console.WriteLine($" {EngineName} ({RuntimeVersion}) — MASTER TECHNICAL SPECIFICATION");
            System.Console.WriteLine("================================================================================");
            System.Console.WriteLine($" * Schema Version     : {SchemaVersion}");
            System.Console.WriteLine($" * Format Version     : {FormatVersion}");
            System.Console.WriteLine($" * Coordinate Space   : {CoordinateSpace}");
            System.Console.WriteLine($" * Scar Record Size   : {ScarRecordSize} bytes");
            System.Console.WriteLine($" * Header Size        : {HeaderSize} bytes");
            System.Console.WriteLine(" * Fundamental Axiom  : Emotion = Physics = Magic = Biology = Architecture");
            System.Console.WriteLine("================================================================================");
        }
    }
}
// ==============================================================================
// END OF FILE: CathedralEngineMasterSpecification.cs
// ==============================================================================
