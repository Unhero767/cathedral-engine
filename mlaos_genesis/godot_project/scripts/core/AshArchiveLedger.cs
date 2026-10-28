using Godot;
using System;
using System.Security.Cryptography;
using System.Text;

/// <summary>
/// Merkle DAG State Management.
/// Persists roster assets, inventory payloads, and structural degradation.
/// Spectral Constant: Blue (Sorrow / Decay)
/// </summary>
public partial class AshArchiveLedger : Node
{
    private string _currentRootHash = string.Empty;

    public string ComputeStratumHash(string payload)
    {
        using (SHA256 sha256 = SHA256.Create())
        {
            byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(payload));
            StringBuilder builder = new StringBuilder();
            foreach (byte b in bytes)
            {
                builder.Append(b.ToString("x2"));
            }
            return builder.ToString();
        }
    }

    public void AppendToDAG(string entityState)
    {
        string newStratum = ComputeStratumHash(entityState + _currentRootHash);
        _currentRootHash = newStratum;
        GD.Print($"[Blue] Entity fossilized into Ash Archive. New Root: {_currentRootHash}");
    }
}
