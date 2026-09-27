using System;
using System.Collections.Generic;
using System.Numerics;

namespace CathedralEngine.Solvers.Topological
{
    public class DiscreteLaplacianSolver
    {
        public float FiedlerFloor { get; set; } = 0.05f;
        public float NominalFiedlerTarget { get; set; } = 0.15f;
        public double PlanckCutoffScale { get; set; } = 1.0e-4;

        private int _nodeCount;
        private readonly List<Vector2> _nodePositions = new List<Vector2>();
        private readonly Dictionary<int, Dictionary<int, float>> _adjacency = new Dictionary<int, Dictionary<int, float>>();

        public float LastComputedFiedler { get; private set; } = 0.0f;
        public bool IsTopologicallyConnected => LastComputedFiedler >= FiedlerFloor;

        public event Action<float>? OnFiedlerCriticalWarning;
        public event Action<int, int, float>? OnXHebbianEdgeSpawned;

        public void InitializeGraph(int initialNodeCount)
        {
            _nodeCount = initialNodeCount;
            _nodePositions.Clear();
            _adjacency.Clear();
            for (int i = 0; i < _nodeCount; i++)
            {
                _nodePositions.Add(Vector2.Zero);
                _adjacency[i] = new Dictionary<int, float>();
            }
        }

        public void SetNodePosition(int nodeIndex, Vector2 position)
        {
            if (nodeIndex >= 0 && nodeIndex < _nodePositions.Count)
            {
                _nodePositions[nodeIndex] = position;
            }
            else if (nodeIndex == _nodePositions.Count)
            {
                _nodePositions.Add(position);
            }
        }

        public void AddOrUpdateEdge(int u, int v, float weight)
        {
            if (u == v || u >= _nodeCount || v >= _nodeCount) return;

            if (u < _nodePositions.Count && v < _nodePositions.Count)
            {
                float distance = Vector2.Distance(_nodePositions[u], _nodePositions[v]);
                if (distance < PlanckCutoffScale)
                {
                    weight = MathF.Min(weight, 1.0f);
                }
            }

            _adjacency[u][v] = weight;
            _adjacency[v][u] = weight;
        }

        public void RemoveEdge(int u, int v)
        {
            if (_adjacency.ContainsKey(u)) _adjacency[u].Remove(v);
            if (_adjacency.ContainsKey(v)) _adjacency[v].Remove(u);
        }

        public float ComputeFiedlerValue(int maxIterations = 50, float tolerance = 1e-4f)
        {
            if (_nodeCount < 2) return 0.0f;

            float[] degrees = new float[_nodeCount];
            for (int i = 0; i < _nodeCount; i++)
            {
                float sum = 0.0f;
                foreach (var kvp in _adjacency[i])
                    sum += kvp.Value;
                degrees[i] = sum;
            }

            float[] v = new float[_nodeCount];
            var rng = new Random(119);
            float mean = 0.0f;
            for (int i = 0; i < _nodeCount; i++)
            {
                v[i] = (float)rng.NextDouble() - 0.5f;
                mean += v[i];
            }
            mean /= _nodeCount;

            float norm = 0.0f;
            for (int i = 0; i < _nodeCount; i++)
            {
                v[i] -= mean;
                norm += v[i] * v[i];
            }
            norm = MathF.Sqrt(norm);
            if (norm > 0)
            {
                for (int i = 0; i < _nodeCount; i++) v[i] /= norm;
            }

            float maxDegree = 0.0f;
            for (int i = 0; i < _nodeCount; i++)
                if (degrees[i] > maxDegree) maxDegree = degrees[i];

            float shift = 2.0f * maxDegree;
            float[] w = new float[_nodeCount];

            for (int iter = 0; iter < maxIterations; iter++)
            {
                for (int i = 0; i < _nodeCount; i++)
                {
                    float av = 0.0f;
                    foreach (var edge in _adjacency[i])
                    {
                        av += edge.Value * v[edge.Key];
                    }
                    w[i] = (shift - degrees[i]) * v[i] + av;
                }

                float proj = 0.0f;
                for (int i = 0; i < _nodeCount; i++) proj += w[i];
                proj /= _nodeCount;
                for (int i = 0; i < _nodeCount; i++) w[i] -= proj;

                norm = 0.0f;
                for (int i = 0; i < _nodeCount; i++) norm += w[i] * w[i];
                norm = MathF.Sqrt(norm);
                if (norm < 1e-9f) break;

                for (int i = 0; i < _nodeCount; i++) v[i] = w[i] / norm;
            }

            float rayleighNumerator = 0.0f;
            for (int i = 0; i < _nodeCount; i++)
            {
                foreach (var edge in _adjacency[i])
                {
                    int j = edge.Key;
                    if (i < j)
                    {
                        float diff = v[i] - v[j];
                        rayleighNumerator += edge.Value * diff * diff;
                    }
                }
            }

            LastComputedFiedler = rayleighNumerator;

            if (LastComputedFiedler < FiedlerFloor)
            {
                OnFiedlerCriticalWarning?.Invoke(LastComputedFiedler);
                InjectXHebbianReinforcement(v);
            }

            return LastComputedFiedler;
        }

        private void InjectXHebbianReinforcement(float[] fiedlerVector)
        {
            int minPositiveNode = -1;
            int maxNegativeNode = -1;
            float minPosVal = float.MaxValue;
            float maxNegVal = float.MinValue;

            for (int i = 0; i < _nodeCount; i++)
            {
                if (fiedlerVector[i] >= 0 && fiedlerVector[i] < minPosVal)
                {
                    minPosVal = fiedlerVector[i];
                    minPositiveNode = i;
                }
                else if (fiedlerVector[i] < 0 && fiedlerVector[i] > maxNegVal)
                {
                    maxNegVal = fiedlerVector[i];
                    maxNegativeNode = i;
                }
            }

            if (minPositiveNode != -1 && maxNegativeNode != -1)
            {
                float restorativeWeight = NominalFiedlerTarget * 1.5f;
                AddOrUpdateEdge(minPositiveNode, maxNegativeNode, restorativeWeight);
                OnXHebbianEdgeSpawned?.Invoke(minPositiveNode, maxNegativeNode, restorativeWeight);
            }
        }
    }
}
