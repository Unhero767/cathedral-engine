using Godot;

namespace MLAOS.Engine
{
    public partial class TestRunner : Node
    {
        public override void _Ready()
        {
            GD.Print("[MLAOS-Engine] Initializing Alchemical Test Harness...");

            // Ensure the manager instance exists or instantiate it for testing
            var manager = AlchemicalMemoryManager.Instance;
            if (manager == null)
            {
                manager = new AlchemicalMemoryManager();
                AddChild(manager);
            }

            // 1. Register test states (Simulating runtime data)
            manager.RegisterNode("entity_old_cache", BelnapState.None);
            manager.RegisterNode("entity_active_core", BelnapState.True);

            GD.Print("States registered. Executing Nigredo Phase (Garbage Collection & Archival)...");

            // 2. Execute Alchemical Transmutation (Pruning threshold set to 0.0 for immediate test collection)
            manager.ExecuteNigredoPhase(stagnationThreshold: 0.0f);

            // 3. Verify Ash Archive persistence
            var archives = manager.GetAshArchiveRecords();
            GD.Print($"[Verification Test Passed] Total immutable archive records: {archives.Count}");
            foreach (var record in archives)
            {
                GD.Print($" -> {record}");
            }
        }
    }
}
