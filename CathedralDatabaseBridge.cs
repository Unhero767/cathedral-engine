// ==============================================================================
// Cathedral-Engine Godot 4 C# Database Bridge Autoload
// File: CathedralDatabaseBridge.cs
// ==============================================================================

using Godot;
using System;
using System.IO;
using Microsoft.Data.Sqlite;

namespace CathedralEngine.Core
{
    public partial class CathedralDatabaseBridge : Node
    {
        public static CathedralDatabaseBridge Instance { get; private set; }

        private string _dbPath;
        private string _connectionString;

        public override void _Ready()
        {
            if (Instance != null && Instance != this)
            {
                QueueFree();
                return;
            }

            Instance = this;
            CallDeferred(nameof(InitializeDatabaseConnection));
        }

        private void InitializeDatabaseConnection()
        {
            // Resolve path relative to project directory
            _dbPath = ProjectSettings.GlobalizePath("res://strata/cathedral_engine.db");
            _connectionString = $"Data Source={_dbPath}";

            GD.Print($"[CATHE_BRIDGE] Initialized SQLite connection at: {_dbPath}");
            
            // Verify table accessibility
            using var connection = new SqliteConnection(_connectionString);
            connection.Open();
            using var command = connection.CreateCommand();
            command.CommandText = "SELECT COUNT(*) FROM stable_characters;";
            long count = (long)command.ExecuteScalar();
            GD.Print($"[CATHE_BRIDGE] Persistent roster link verified. Stable characters registered: {count}");
        }

        public void UpdateCharacterPosition(string characterId, Vector3 newPosition, float somaticStress)
        {
            using var connection = new SqliteConnection(_connectionString);
            connection.Open();

            using var command = connection.CreateCommand();
            command.CommandText = @"
                UPDATE stable_characters 
                SET pos_x = @posX, 
                    pos_y = @posY, 
                    pos_z = @posZ, 
                    somatic_stress = @stress,
                    updated_at = CURRENT_TIMESTAMP
                WHERE character_id = @charId;
            ";

            command.Parameters.AddWithValue("@posX", newPosition.X);
            command.Parameters.AddWithValue("@posY", newPosition.Y);
            command.Parameters.AddWithValue("@posZ", newPosition.Z);
            command.Parameters.AddWithValue("@stress", somaticStress);
            command.Parameters.AddWithValue("@charId", characterId);

            int rowsAffected = command.ExecuteNonQuery();
            if (rowsAffected > 0)
            {
                GD.Print($"[CATHE_BRIDGE] Synchronized [{characterId}] position -> X:{newPosition.X:F2}, Y:{newPosition.Y:F2}, Z:{newPosition.Z:F2}");
            }
        }
    }
}
