using System.Collections.Generic;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Codifies the three-tier product architecture mapping the 40-Book Codex framework
    /// across physical, collectible, and interactive digital substrates.
    /// </summary>
    public static class ProductArchitectureRegistry
    {
        public static readonly Dictionary<string, string> Tiers = new()
        {
            { "Tier_1_Oracle", "40-Card Living Arcana Oracle Deck (Physical collectible deck mapping major theological/ontological arcana)" },
            { "Tier_2_Codex", "4-Volume Hardcover Codex Box Set (Prime Foundations, Inner Mandala, Outer Choirs, Inner Shadow Canon)" },
            { "Tier_3_Engine", "Interactive WebGL & Godot 4 System Engine (Dual-topology runtime rendering spatialized .mlvox architectural vaults)" }
        };

        public static void PrintManifest()
        {
            System.Console.WriteLine("================================================================================");
            System.Console.WriteLine(" CATHEDRAL-ENGINE THREE-TIER PRODUCT ARCHITECTURE MANIFEST");
            System.Console.WriteLine("================================================================================");
            foreach (var tier in Tiers)
            {
                System.Console.WriteLine($" - [{tier.Key}]: {tier.Value}");
            }
            System.Console.WriteLine("================================================================================");
        }
    }
}
// ==============================================================================
// END OF FILE: ProductArchitectureRegistry.cs
// ==============================================================================
