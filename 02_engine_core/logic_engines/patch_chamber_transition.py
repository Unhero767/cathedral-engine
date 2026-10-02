import jax
import jax.numpy as jnp

@jax.jit
def apply_linear_genesis_transition(state_tensor, history_tensor, choice_tensor, evidence_tensor, pressure_tensor, kappa=0.015, mu=0.008, dt=0.01):
    """
    Computes Sn+1 = R(Sn, Hn, Cn, En, Pn) incorporating the Clausius dissipation tensor
    and Belnap-Dunn paraconsistent integration rules.
    """
    grad_z, grad_y, grad_x = jnp.gradient(state_tensor)
    grad_sq = grad_x**2 + grad_y**2 + grad_z**2
    
    velocity_gradients = jnp.gradient(choice_tensor, axis=(1, 2, 3)) if choice_tensor.ndim == 4 else jnp.gradient(choice_tensor)
    velocity_grad_sq = sum(g**2 for g in velocity_gradients)
    velocity_grad_mag_sq = jnp.sum(velocity_grad_sq, axis=0) if velocity_grad_sq.ndim == 4 else velocity_grad_sq
    
    dq_diss = kappa * grad_sq + mu * velocity_grad_mag_sq
    ds = dq_diss * dt
    
    updated_history = history_tensor + ds
    integrated_state = jnp.maximum(0.0, state_tensor - 0.05 * updated_history + 0.01 * evidence_tensor - 0.02 * pressure_tensor)
    return integrated_state, updated_history
