using Godot;
using System;
using System.Collections.Generic;
using System.Linq;

namespace MLAOS.Engine
{
    public enum BelnapState
    {
        True,
        False,
        Both,
        None
    }

    public class StateNode
    {
        public string Id { get; set; }
        public BelnapState State { get; set; }
        public float Age { get; set; }
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    public partial class AlchemicalMemoryManager : Node
    {
        public static AlchemicalMemoryManager Instance { get; private set; }

        private readonly Dictionary<string, StateNode> _stateBuffer = new();
        private readonly List<string> _ashArchiveLedger = new();

        public override void _Ready()
        {
            Instance = this;
            GD.Print("[MLAOS-Engine] AlchemicalMemoryManager initialized. Ready for runtime transmutation.");
        }

        public void RegisterNode(string id, BelnapState state, Dictionary<string, object> metadata = null)
        {
            if (_stateBuffer.ContainsKey(id))
            {
                _stateBuffer[id].State = state;
                _stateBuffer[id].Age = 0.0f;
                if (metadata != null) _stateBuffer[id].Metadata = metadata;
            }
            else
            {
                _stateBuffer.Add(id, new StateNode
                {
                    Id = id,
                    State = state,
                    Age = 0.0f,
                    Metadata = metadata ?? new()
                });
            }
        }

        public override void _Process(double delta)
        {
            foreach (var node in _stateBuffer.Values)
            {
                node.Age += (float)delta;
            }
        }

        public void ExecuteNigredoPhase(float stagnationThreshold = 10.0f)
        {
            var targetKeys = _stateBuffer.Values
                .Where(node => node.State == BelnapState.None && node.Age >= stagnationThreshold)
                .Select(node => node.Id)
                .ToList();

            int purgedCount = 0;
            foreach (var key in targetKeys)
            {
                var node = _stateBuffer[key];
                string archiveRecord = $"[ARCHIVE_COMMITTED] ID: {node.Id} | Transmuted to Harmonic Scar at time {Engine.GetProcessFrames()}";
                _ashArchiveLedger.Add(archiveRecord);
                GD.Print(archiveRecord);

                _stateBuffer.Remove(key);
                purgedCount++;
            }

            if (purgedCount > 0)
            {
                GD.Print($"[Alchemical Interior] Nigredo Phase complete. Pruned {purgedCount} obsolete nodes. Memory compacted.");
            }
        }

        public IReadOnlyList<string> GetAshArchiveRecords() => _ashArchiveLedger.AsReadOnly();
    }
}
