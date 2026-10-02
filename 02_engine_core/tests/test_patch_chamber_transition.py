import jax
import jax.numpy as jnp
import pytest
from logic_engines.patch_chamber_transition import apply_linear_genesis_transition

def test_linear_genesis_transition():
    dim = 16
    key = jax.random.PRNGKey(42)
    
    state_tensor = jax.random.uniform(key, (dim, dim, dim), dtype=jnp.float32)
    history_tensor = jnp.zeros((dim, dim, dim), dtype=jnp.float32)
    choice_tensor = jax.random.uniform(key, (3, dim, dim, dim), dtype=jnp.float32)
    evidence_tensor = jnp.ones((dim, dim, dim), dtype=jnp.float32) * 0.5
    pressure_tensor = jnp.ones((dim, dim, dim), dtype=jnp.float32) * 0.1
    
    next_state, next_history = apply_linear_genesis_transition(
        state_tensor, history_tensor, choice_tensor, evidence_tensor, pressure_tensor
    )
    
    assert next_state.shape == (dim, dim, dim)
    assert next_history.shape == (dim, dim, dim)
    assert jnp.all(next_state >= 0.0)
