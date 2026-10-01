#!/usr/bin/env bash
# MLAOS-Prime :: C# Paraconsistent Solver Scaffolding (.NET 10)
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

echo -e "\033[1;36m┌────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│   Σ-7 :: FORGING C# LOGIC SOLVERS      │\033[0m"
echo -e "\033[1;36m└────────────────────────────────────────┘\033[0m"

# 0. Clean previous partial generation
rm -f CathedralEngine.sln
rm -rf CathedralEngine.Solvers

# 1. Initialize Solution and Class Library (Targeting net10.0)
dotnet new sln -n CathedralEngine
dotnet new classlib -n CathedralEngine.Solvers -f net10.0
dotnet sln CathedralEngine.sln add CathedralEngine.Solvers/CathedralEngine.Solvers.csproj

# 2. Forge the Belnap-Dunn 4-Valued Matrix
cat << 'CS_EOF' > CathedralEngine.Solvers/BelnapDunnMatrix.cs
using System;

namespace CathedralEngine.Solvers
{
    public enum TruthValue : byte
    {
        None = 0,   // Neither (N)
        False = 1,  // False (F)
        True = 2,   // True (T)
        Both = 3    // Both (B) - Dialetheic Contradiction
    }

    public static class BelnapDunnMatrix
    {
        /// <summary>
        /// Evaluates the Truth Meet (Conjunction) of two paraconsistent claims.
        /// </summary>
        public static TruthValue EvaluateConjunction(TruthValue a, TruthValue b)
        {
            if (a == TruthValue.False || b == TruthValue.False) return TruthValue.False;
            if (a == TruthValue.True && b == TruthValue.True) return TruthValue.True;
            if (a == b) return a;
            return TruthValue.False; // Fallback for asymmetric contradictions
        }

        /// <summary>
        /// Metamorphic Squeeze logic: Returns the crystallization angle when Both (B) is synthesized.
        /// </summary>
        public static double CalculateSqueezeAngle(TruthValue claimA, TruthValue claimB)
        {
            if (claimA == TruthValue.Both || claimB == TruthValue.Both || 
               (claimA == TruthValue.True && claimB == TruthValue.False) || 
               (claimA == TruthValue.False && claimB == TruthValue.True))
            {
                return 54.74; // Ideal obsidian crystallization angle
            }
            return 0.0; // No fracture detected
        }
    }
}
CS_EOF

# Remove default template boilerplate
rm -f CathedralEngine.Solvers/Class1.cs

# 3. Compile the Release Build
echo -e "\n\033[1;33m[i] Compiling CathedralEngine.Solvers...\033[0m"
dotnet build CathedralEngine.sln -c Release

echo -e "\n\033[1;32m[✓] C# Solvers Compiled. Run 'studio build' to recompile via orchestrator.\033[0m"
