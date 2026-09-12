using Godot;
using System;

namespace MLAOS.Runtime
{
    public static class VoxelTextureBuilder
    {
        public static ImageTexture3D CreateVolumeTexture(int resolution, float[] occupancyGrid)
        {
            if (occupancyGrid.Length != resolution * resolution * resolution)
            {
                throw new ArgumentException("Occupancy grid length does not match resolution dimensions.");
            }

            int size = resolution;
            var data = new byte[size * size * size * 4];

            for (int z = 0; z < size; z++)
            {
                for (int y = 0; y < size; y++)
                {
                    for (int x = 0; x < size; x++)
                    {
                        int index = x + (y * size) + (z * size * size);
                        float val = occupancyGrid[index];
                        byte[] floatBytes = BitConverter.GetBytes(val);
                        int byteOffset = index * 4;
                        Buffer.BlockCopy(floatBytes, 0, data, byteOffset, 4);
                    }
                }
            }

            var image = Image.CreateFromData(size, size * size, false, Image.Format.Rf, data);
            var texture3D = new ImageTexture3D();
            texture3D.Create(Image.Format.Rf, size, size, size, false, new Godot.Collections.Array<Image> { image });

            return texture3D;
        }
    }
}
// ==============================================================================
// END OF FILE: VoxelTextureBuilder.cs
// ==============================================================================
