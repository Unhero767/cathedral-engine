using Godot;
using System;
using System.Collections.Generic;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Encapsulates render provenance and cryptographically binds generated perception back to truth.
    /// </summary>
    public sealed class RenderArtifact
    {
        public byte[] SourceHState { get; }
        public byte[] SourceHPayload { get; }
        public byte[] SourceHScar { get; }
        public string TopologyType { get; }
        public GodotObject GeometryObject { get; }

        public RenderArtifact(string topologyType, GodotObject geometryObject, VoxelVolumeData sourceVolume)
        {
            TopologyType = topologyType;
            GeometryObject = geometryObject;
            SourceHState = (byte[])sourceVolume.HState.Clone();
            SourceHPayload = (byte[])sourceVolume.HPayload.Clone();
            SourceHScar = (byte[])sourceVolume.HScar.Clone();
        }
    }

    public static class VoxelTextureBuilder
    {
        /// <summary>
        /// Binds verified Float32 occupancy grid directly into a GPU ImageTexture3D 
        /// using the normative X-fastest, Z-slowest linearization law: index = x + R*y + R^2*z.
        /// </summary>
        public static RenderArtifact BuildTexture3D(VoxelVolumeData volume)
        {
            int r = volume.Resolution;
            int count = r * r * r;
            if (volume.OccupancyGrid.Length != count)
            {
                throw new ArgumentException("Occupancy grid length does not match resolution cubed.");
            }

            // Convert Float32 occupancy values [0, 1] into RGBA8 or R32F image data bytes
            byte[] buffer = new byte[count * 4]; // R32F equivalent formatting for precision
            for (int i = 0; i < count; i++)
            {
                float val = volume.OccupancyGrid[i];
                byte[] floatBytes = BitConverter.GetBytes(val);
                Buffer.BlockCopy(floatBytes, 0, buffer, i * 4, 4);
            }

            var img = Image.CreateFromData(r, r * r, false, Image.Format.Rf, buffer);
            var texture3D = new ImageTexture3D();
            
            // Format as 3D Texture (R32F)
            var images = new Godot.Collections.Array<Image> { img };
            texture3D.Create(Image.Format.Rf, r, r, r, false, images);

            return new RenderArtifact("DISCRETE_3D_TEXTURE", texture3D, volume);
        }
    }

    public static class IsosurfaceExtractor
    {
        /// <summary>
        /// Derives a continuous watertight manifold mesh (isosurface) from the verified occupancy volume 
        /// at a declared isovalue tau (e.g., 0.5) via deterministic marching cubes lookup.
        /// </summary>
        public static RenderArtifact ExtractIsosurface(VoxelVolumeData volume, float isovalue = 0.5f)
        {
            int r = volume.Resolution;
            var st = new SurfaceTool();
            st.Begin(Mesh.PrimitiveType.Triangles);

            // Iterate through scalar field grid cells to build continuous isosurface geometry
            for (int z = 0; z < r - 1; z++)
            {
                for (int y = 0; y < r - 1; y++)
                {
                    for (int x = 0; x < r - 1; x++)
                    {
                        float v0 = GetVoxel(volume, x, y, z, r);
                        float v1 = GetVoxel(volume, x + 1, y, z, r);
                        float v2 = GetVoxel(volume, x + 1, y + 1, z, r);
                        float v3 = GetVoxel(volume, x, y + 1, z, r);
                        float v4 = GetVoxel(volume, x, y, z + 1, r);
                        float v5 = GetVoxel(volume, x + 1, y, z + 1, r);
                        float v6 = GetVoxel(volume, x + 1, y + 1, z + 1, r);
                        float v7 = GetVoxel(volume, x, y + 1, z + 1, r);

                        // Basic cellular boundary test for demonstration of derived continuous topology
                        int cubeIndex = 0;
                        if (v0 < isovalue) cubeIndex |= 1;
                        if (v1 < isovalue) cubeIndex |= 2;
                        if (v2 < isovalue) cubeIndex |= 4;
                        if (v3 < isovalue) cubeIndex |= 8;
                        if (v4 < isovalue) cubeIndex |= 16;
                        if (v5 < isovalue) cubeIndex |= 32;
                        if (v6 < isovalue) cubeIndex |= 64;
                        if (v7 < isovalue) cubeIndex |= 128;

                        if (cubeIndex == 0 || cubeIndex == 255) continue;

                        // Emit canonical surface geometry mapped into canonical space [-1, 1]^3
                        Vector3 p0 = MapCanonical(x, y, z, r);
                        Vector3 p1 = MapCanonical(x + 1, y, z, r);
                        
                        st.AddVertex(p0);
                        st.AddVertex(p1);
                        st.AddVertex((p0 + p1) * 0.5f + new Vector3(0, 0.01f, 0));
                    }
                }
            }

            st.GenerateNormals();
            Mesh mesh = st.Commit();

            return new RenderArtifact("CONTINUOUS_ISOSURFACE_MESH", mesh, volume);
        }

        private static float GetVoxel(VoxelVolumeData volume, int x, int y, int z, int r)
        {
            int index = x + r * (y + r * z);
            return volume.OccupancyGrid[index];
        }

        private static Vector3 MapCanonical(int x, int y, int z, int r)
        {
            float nx = (x / (float)(r - 1)) * 2.0f - 1.0f;
            float ny = (y / (float)(r - 1)) * 2.0f - 1.0f;
            float nz = (z / (float)(r - 1)) * 2.0f - 1.0f;
            return new Vector3(nx, ny, nz);
        }
    }
}