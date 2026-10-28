using System;
using System.Collections.Generic;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;

namespace CathedralEngine.Solvers.Paraconsistent
{
    public enum BelnapTruthValue { N = 0, F = 1, T = 2, B = 3 }

    public struct DialetheicCell
    {
        public BelnapTruthValue Truth;
        public Vector2 StressTensorPrincipal;
        public float ShearStress;
        public float OrientationAngle;
        public bool IsPermineralized;
    }

    public class GkslMasterDissipator
    {
        public static readonly float MagicAngle = MathF.Acos(1.0f / MathF.Sqrt(3.0f));

        public float PyragasGainK { get; set; } = 0.384f;
        public float CriticalGainK { get; set; } = 0.750f;
        public float EpistemicRemainderDelta { get; set; } = 0.001f;

        private readonly Queue<Vector2> _stateHistory = new Queue<Vector2>();
        private const int HistoryDelayTicks = 11;

        public string CurrentMerkleRoot { get; private set; } = "0000000000000000000000000000000000000000000000000000000000000000";

        public bool IsMagicAngleAligned(float angle, float tolerance = 0.02f)
        {
            float delta = MathF.Abs(angle - MagicAngle);
            return delta <= tolerance;
        }

        public Vector2 ApplyPyragasStabilization(Vector2 currentCoordinate)
        {
            _stateHistory.Enqueue(currentCoordinate);
            if (_stateHistory.Count < HistoryDelayTicks)
                return Vector2.Zero;

            Vector2 delayedCoordinate = _stateHistory.Dequeue();

            float perturbationNormSq = Vector2.DistanceSquared(currentCoordinate, delayedCoordinate);
            float saturatedGain = PyragasGainK / (1.0f + 2.5f * perturbationNormSq);

            if (saturatedGain >= CriticalGainK)
            {
                saturatedGain = CriticalGainK - 0.05f;
            }

            return saturatedGain * (delayedCoordinate - currentCoordinate);
        }

        public DialetheicCell ExecuteMetamorphicSqueeze(DialetheicCell cell, int cellIndex)
        {
            if (cell.Truth != BelnapTruthValue.B) return cell;

            cell.OrientationAngle = MagicAngle;
            cell.ShearStress = 0.0f;

            float meanStress = (cell.StressTensorPrincipal.X + cell.StressTensorPrincipal.Y) * 0.5f;
            cell.StressTensorPrincipal = new Vector2(meanStress, meanStress);
            cell.IsPermineralized = true;

            CommitToAshArchive(cellIndex, cell);

            return cell;
        }

        private void CommitToAshArchive(int cellId, DialetheicCell scar)
        {
            string payload = $"{CurrentMerkleRoot}|ID:{cellId}|TRUTH:{scar.Truth}|STRESS:{scar.StressTensorPrincipal.X:F4}|REM:{EpistemicRemainderDelta}";
            using SHA256 sha = SHA256.Create();
            byte[] hashBytes = sha.ComputeHash(Encoding.UTF8.GetBytes(payload));
            CurrentMerkleRoot = BitConverter.ToString(hashBytes).Replace("-", "").ToLowerInvariant();
        }
    }
}
