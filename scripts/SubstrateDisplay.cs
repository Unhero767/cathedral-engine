using Godot;
using System;
using CathedralEngine.Core.Substrate;

namespace CathedralEngine.Core
{
    [GlobalClass]
    public partial class SubstrateDisplay : TextureRect
    {
        [Export] public NodePath? EnginePath { get; set; }

        private MlaosSubstrateEngine? _engine;
        private Image _image = null!;
        private ImageTexture _texture = null!;
        private byte[] _pixelBuffer = null!;

        public override void _Ready()
        {
            if (EnginePath != null)
                _engine = GetNodeOrNull<MlaosSubstrateEngine>(EnginePath);

            int width = _engine?.GridWidth ?? 256;
            int height = _engine?.GridHeight ?? 256;

            _pixelBuffer = new byte[width * height * 4];
            _image = Image.CreateEmpty(width, height, false, Image.Format.Rgba8);
            _texture = ImageTexture.CreateFromImage(_image);
            Texture = _texture;
        }

        public override void _Process(double delta)
        {
            if (_engine == null) return;

            _engine.CopyBufferToRgba(_pixelBuffer);
            _image.SetData(_engine.GridWidth, _engine.GridHeight, false, Image.Format.Rgba8, _pixelBuffer);
            _texture.Update(_image);
        }
    }
}
