class_name DPT64Types
extends Node

enum CellType { EMPTY, WALL, DOOR, TRAP, STAIRS_DOWN, STAIRS_UP }
enum DamageType { KINETIC, SPECTRAL, VOID, CALORIC }
enum TorchSpectrum { GOLD = 580, CYAN = 620, CRIMSON = 430, OBSIDIAN = 0 }

const TORCH_NAMES = {
    TorchSpectrum.GOLD: "Gold Theta",
    TorchSpectrum.CYAN: "Cyan Psi",
    TorchSpectrum.CRIMSON: "Crimson Phi",
    TorchSpectrum.OBSIDIAN: "Obsidian Void"
}
