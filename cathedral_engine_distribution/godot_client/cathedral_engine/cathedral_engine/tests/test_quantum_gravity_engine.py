import unittest
import math
from pathlib import Path
import sys

ENGINE_ROOT = Path(__file__).resolve().parent.parent
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from engines.quantum_gravity_engine import (
    QuantumGravityEngine,
    SchrodingerNewtonSolver,
    QuantumGravityLatticeComponent,
    ComplexArray,
    HBAR_DEFAULT,
    G_DEFAULT
)


class TestQuantumGravityEngine(unittest.TestCase):
    def setUp(self):
        self.grid_size = 16
        self.dx = 1.0e-15
        self.mass = 1.0e-20
        self.engine = QuantumGravityEngine(
            grid_size=self.grid_size,
            dx=self.dx,
            mass=self.mass
        )

    def test_lattice_initialization_and_norm(self):
        comp = self.engine.component
        num_cells = self.grid_size * self.grid_size
        self.assertEqual(len(comp.psi.real), num_cells)
        self.assertEqual(len(comp.psi.imag), num_cells)

        # Verify wavefunction normalization: integral |psi|^2 dV = 1
        norm = sum((comp.psi.real[i] ** 2 + comp.psi.imag[i] ** 2) * (self.dx * self.dx) for i in range(num_cells))
        self.assertAlmostEqual(norm, 1.0, places=5)

    def test_fft_round_trip(self):
        solver = self.engine.solver
        n = self.grid_size
        num_cells = n * n
        re = [math.sin(i * 0.5) for i in range(num_cells)]
        im = [math.cos(i * 0.3) for i in range(num_cells)]

        orig_re = list(re)
        orig_im = list(im)

        solver._fft_2d(re, im, inverse=False)
        solver._fft_2d(re, im, inverse=True)

        for i in range(num_cells):
            self.assertAlmostEqual(re[i], orig_re[i], places=6)
            self.assertAlmostEqual(im[i], orig_im[i], places=6)

    def test_gravitational_self_potential_and_strain(self):
        comp = self.engine.component
        self.engine.solver.update_gravitational_self_potential(comp)

        # Gravitational self-potential should be negative in real space (attractive well)
        # Note: Green's function convolution with -1/k^2 produces attractive self-potential
        self.assertLessEqual(comp.total_self_energy, 0.0)

        # Medium strain epsilon(r) must be in [0, 1)
        for eps in comp.strain_field:
            self.assertGreaterEqual(eps, 0.0)
            self.assertLess(eps, 1.0)

    def test_split_step_fourier_evolution(self):
        comp = self.engine.component
        dt = 1.0e-18
        num_cells = self.grid_size * self.grid_size

        initial_energy = comp.total_self_energy
        self.engine.solver.time_step(comp, dt)

        # Check that norm is preserved
        norm = sum((comp.psi.real[i] ** 2 + comp.psi.imag[i] ** 2) * (self.dx * self.dx) for i in range(num_cells))
        self.assertAlmostEqual(norm, 1.0, places=5)

        # Telemetry should be active
        self.assertNotEqual(comp.total_self_energy, 0.0)

    def test_diosi_penrose_decoherence(self):
        displacement = 1.0e-14
        dp = self.engine.calculate_diosi_penrose_decoherence(displacement)

        self.assertEqual(dp["mass_kg"], self.mass)
        self.assertEqual(dp["displacement_m"], displacement)
        self.assertGreater(dp["delta_e_g_joules"], 0.0)
        self.assertGreater(dp["tau_decay_seconds"], 0.0)

        expected_delta_e = (2.0 * G_DEFAULT * (self.mass ** 2)) / displacement
        self.assertAlmostEqual(dp["delta_e_g_joules"], expected_delta_e, delta=expected_delta_e * 0.01)

    def test_autopoietic_effective_mass(self):
        m0 = 1.0e-20
        # When epsilon = 0, m*(0) = m0
        m_eff_0 = self.engine.compute_autopoietic_effective_mass(0.0, m0)
        self.assertAlmostEqual(m_eff_0, m0, places=25)

        # When epsilon = 0.6, m*(0.6) = m0 / sqrt(1 - 0.36) = m0 / 0.8 = 1.25 * m0
        m_eff_06 = self.engine.compute_autopoietic_effective_mass(0.6, m0)
        self.assertAlmostEqual(m_eff_06, 1.25 * m0, places=24)

    def test_qgrav_functor_evaluation(self):
        qgrav_res = self.engine.evaluate_qgrav_functor()
        self.assertEqual(qgrav_res["category"], "QGrav")
        self.assertEqual(qgrav_res["functor"], "SelfConsistencyFunctor_S")
        self.assertIn("is_fixed_point_soliton", qgrav_res)
        self.assertIn("verdict", qgrav_res)


if __name__ == "__main__":
    unittest.main()
