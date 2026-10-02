import jax
import jax.numpy as jnp
import pytest

@jax.jit
def clausius_voxel_baking_kernel(density_grid, velocity_field, entropy_buffer, kappa, mu, dt):
    grad_density_z, grad_density_y, grad_density_x = jnp.gradient(density_grid)
    grad_density_sq = grad_density_x**2 + grad_density_y**2 + grad_density_z**2
    
    velocity_gradients = jnp.gradient(velocity_field, axis=(1, 2, 3))
    velocity_grad_sq = sum(g**2 for g in velocity_gradients)
    velocity_grad_mag_sq = jnp.sum(velocity_grad_sq, axis=0)
    
    dq_diss = kappa * grad_density_sq + mu * velocity_grad_mag_sq
    ds = dq_diss * dt
    updated_entropy = entropy_buffer + ds
    attenuated_density = jnp.maximum(0.0, density_grid - 0.05 * updated_entropy)
    return attenuated_density, updated_entropy

def test_clausius_kernel_execution():
    dim = 32
    key = jax.random.PRNGKey(0)
    density_grid = jax.random.uniform(key, (dim, dim, dim), dtype=jnp.float32, minval=0.1, maxval=1.0)
    
    velocity_key, key = jax.random.split(key)
    velocity_field = jax.random.uniform(velocity_key, (3, dim, dim, dim), dtype=jnp.float32, minval=-1.0, maxval=1.0)
    entropy_buffer = jnp.zeros((dim, dim, dim), dtype=jnp.float32)
    
    final_density, final_entropy = clausius_voxel_baking_kernel(
        density_grid, velocity_field, entropy_buffer, 0.015, 0.008, 0.01
    )
    
    assert final_density.shape == (dim, dim, dim)
    assert final_entropy.shape == (dim, dim, dim)
    assert jnp.all(final_density >= 0.0)
