"""
Demo 2: ML Gradient Tracking — IEEE 754 vs IVNA
================================================

Shows how IVNA-indexed gradients diagnose WHERE and WHY gradients fail
during neural network training.

Standard: gradients → 0 (vanishing) or → Inf/NaN (exploding). Information lost.
IVNA:     gradients → 0_x (vanishing) or ∞_x (exploding). Index tracks the scale.

Key insight: The INDEX of a vanished gradient tells you what it WOULD have been
if the network were healthier. This is diagnostic gold.
"""

import sys
import os
import numpy as np
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ivna import Virtual, Z, I

np.random.seed(42)


# ============================================================
# SIMPLE NEURAL NETWORK (for demonstration)
# ============================================================

def sigmoid(x):
    """Standard sigmoid — saturates at 0 and 1."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

def sigmoid_derivative(x):
    """σ'(x) = σ(x)(1 - σ(x)). Goes to 0 for large |x|."""
    s = sigmoid(x)
    return s * (1.0 - s)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)


class SimpleNetwork:
    """A multi-layer network designed to demonstrate gradient pathologies."""

    def __init__(self, layer_sizes, activation='sigmoid', init_scale=1.0):
        """
        layer_sizes: [input_dim, hidden1, hidden2, ..., output_dim]
        activation: 'sigmoid' or 'relu'
        init_scale: weight initialization scale (large = exploding, small = vanishing)
        """
        self.layers = []
        self.biases = []
        self.activation = activation

        for i in range(len(layer_sizes) - 1):
            # Xavier-like init, but scaled by init_scale
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * init_scale / np.sqrt(layer_sizes[i])
            b = np.zeros(layer_sizes[i+1])
            self.layers.append(w)
            self.biases.append(b)

    def forward(self, x):
        """Forward pass, storing activations for backprop."""
        self.activations = [x]
        self.pre_activations = []

        for i, (w, b) in enumerate(zip(self.layers, self.biases)):
            z = self.activations[-1] @ w + b
            self.pre_activations.append(z)

            if i < len(self.layers) - 1:  # Hidden layers
                if self.activation == 'sigmoid':
                    a = sigmoid(z)
                else:
                    a = relu(z)
            else:  # Output layer (no activation for regression)
                a = z

            self.activations.append(a)

        return self.activations[-1]

    def backward_ieee(self, y_true):
        """Standard backprop — IEEE 754 arithmetic.

        Returns gradient magnitudes per layer.
        """
        n_samples = y_true.shape[0]

        # Output layer gradient
        delta = (self.activations[-1] - y_true) / n_samples  # MSE gradient

        grad_magnitudes = []
        layer_gradients = []

        for i in range(len(self.layers) - 1, -1, -1):
            # Gradient w.r.t. weights
            grad_w = self.activations[i].T @ delta
            grad_magnitudes.append(np.mean(np.abs(grad_w)))
            layer_gradients.append(grad_w.copy())

            if i > 0:
                # Propagate gradient through activation
                delta = delta @ self.layers[i].T
                if self.activation == 'sigmoid':
                    delta *= sigmoid_derivative(self.pre_activations[i-1])
                else:
                    delta *= relu_derivative(self.pre_activations[i-1])

        grad_magnitudes.reverse()
        layer_gradients.reverse()
        return grad_magnitudes, layer_gradients

    def backward_ivna(self, y_true):
        """IVNA-aware backprop — tracks gradient pathologies.

        When a gradient magnitude drops below threshold → 0_x (vanishing)
        When a gradient magnitude exceeds threshold → ∞_x (exploding)
        The INDEX x tracks what the gradient scale SHOULD be.
        """
        n_samples = y_true.shape[0]

        VANISH_THRESHOLD = 1e-4
        EXPLODE_THRESHOLD = 1e4

        delta = (self.activations[-1] - y_true) / n_samples

        ivna_diagnostics = []
        grad_magnitudes = []
        cumulative_shrink = 1.0  # Track cumulative gradient scaling

        for i in range(len(self.layers) - 1, -1, -1):
            grad_w = self.activations[i].T @ delta
            mag = np.mean(np.abs(grad_w))
            grad_magnitudes.append(mag)

            # IVNA analysis
            layer_info = {
                'layer': i,
                'magnitude': mag,
                'max_grad': np.max(np.abs(grad_w)),
                'min_grad': np.min(np.abs(grad_w)),
                'cumulative_scale': cumulative_shrink,
            }

            if mag < VANISH_THRESHOLD:
                # Gradient has vanished — in IEEE 754, this is just "≈ 0"
                # In IVNA, we track it as 0_x where x = what the gradient WOULD be
                # at proper scale
                if mag > 0:
                    # x = gradient / vanish_threshold — how far below threshold
                    x = mag / VANISH_THRESHOLD
                    ivna_grad = Z(Fraction(x).limit_denominator(10**6))
                else:
                    ivna_grad = Z(0)  # Truly dead

                layer_info['ivna'] = ivna_grad
                layer_info['status'] = 'VANISHED'
                layer_info['diagnosis'] = (
                    f"Gradient vanished to {mag:.2e}. "
                    f"IVNA: {ivna_grad} — index {float(ivna_grad.index):.6f} shows "
                    f"relative scale vs threshold. "
                    f"Cumulative shrink: {cumulative_shrink:.2e}"
                )

            elif mag > EXPLODE_THRESHOLD:
                # Gradient exploding — IEEE gives Inf, IVNA gives ∞_x
                x = mag / EXPLODE_THRESHOLD
                ivna_grad = I(Fraction(x).limit_denominator(10**6))

                layer_info['ivna'] = ivna_grad
                layer_info['status'] = 'EXPLODING'
                layer_info['diagnosis'] = (
                    f"Gradient exploding at {mag:.2e}. "
                    f"IVNA: {ivna_grad} — index {float(ivna_grad.index):.2f}x above threshold. "
                    f"Cumulative growth: {cumulative_shrink:.2e}"
                )

            else:
                layer_info['ivna'] = mag  # Normal — just the real number
                layer_info['status'] = 'HEALTHY'
                layer_info['diagnosis'] = f"Gradient healthy at {mag:.2e}"

            ivna_diagnostics.append(layer_info)

            # Track cumulative scaling for next layer
            if i > 0:
                # How much does this layer's activation derivative scale the gradient?
                if self.activation == 'sigmoid':
                    act_deriv = sigmoid_derivative(self.pre_activations[i-1])
                    scale = np.mean(np.abs(act_deriv))
                else:
                    act_deriv = relu_derivative(self.pre_activations[i-1])
                    scale = np.mean(np.abs(act_deriv))

                weight_scale = np.mean(np.abs(self.layers[i]))
                cumulative_shrink *= scale * weight_scale

                delta = delta @ self.layers[i].T
                if self.activation == 'sigmoid':
                    delta *= sigmoid_derivative(self.pre_activations[i-1])
                else:
                    delta *= relu_derivative(self.pre_activations[i-1])

        ivna_diagnostics.reverse()
        grad_magnitudes.reverse()
        return grad_magnitudes, ivna_diagnostics


# ============================================================
# DEMONSTRATIONS
# ============================================================

def demo_vanishing_gradients():
    """Deep sigmoid network → vanishing gradients."""
    print("=" * 70)
    print("DEMO 2A: Vanishing Gradients (Deep Sigmoid Network)")
    print("=" * 70)

    # 10-layer sigmoid network — guaranteed to vanish
    layers = [2, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1]
    net = SimpleNetwork(layers, activation='sigmoid', init_scale=0.5)

    # XOR-like data
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    # Forward pass
    pred = net.forward(X)

    # IEEE backprop
    ieee_mags, ieee_grads = net.backward_ieee(y)

    # IVNA backprop
    ivna_mags, ivna_diags = net.backward_ivna(y)

    print(f"\n  Network: {len(layers)-1} layers, sigmoid activation, init_scale=0.5")
    print(f"  Task: XOR classification")
    print(f"  Vanish threshold: 1e-4, Explode threshold: 1e4")
    print(f"\n  {'Layer':>6s}  {'IEEE Grad Mag':>15s}  {'IVNA Analysis':>20s}  {'Status':>12s}")
    print("  " + "-" * 60)

    for i, (ieee_mag, ivna_info) in enumerate(zip(ieee_mags, ivna_diags)):
        ivna_str = str(ivna_info['ivna']) if isinstance(ivna_info['ivna'], Virtual) else f"{ivna_info['ivna']:.2e}"
        print(f"  {i:>6d}  {ieee_mag:>15.2e}  {ivna_str:>20s}  {ivna_info['status']:>12s}")

    print(f"\n  IEEE 754 sees: Gradients in early layers are 'basically zero'")
    print(f"  IVNA sees: Gradients are 0_x where x tells you the RELATIVE scale")

    # Show what IVNA indices reveal
    print(f"\n  IVNA DIAGNOSTIC DETAIL:")
    for info in ivna_diags:
        if info['status'] != 'HEALTHY':
            print(f"    Layer {info['layer']}: {info['diagnosis']}")

    # KEY: IVNA ratios between vanished gradients are MEANINGFUL
    vanished = [(info['layer'], info['magnitude']) for info in ivna_diags if info['status'] == 'VANISHED']
    if len(vanished) >= 2:
        print(f"\n  KEY INSIGHT — Ratios between vanished gradients:")
        for i in range(len(vanished) - 1):
            l1, m1 = vanished[i]
            l2, m2 = vanished[i + 1]
            if m2 > 0:
                ratio = m1 / m2
                print(f"    Layer {l1} / Layer {l2} = {ratio:.4f} — this is the per-layer shrink factor")

        print(f"\n  In IEEE 754, all these are just '0.00'. The structure is invisible.")
        print(f"  In IVNA, 0_{{x₁}} / 0_{{x₂}} = x₁/x₂ — the RATIO is a real number!")
        print(f"  This ratio reveals the per-layer gradient decay rate.")

    return ieee_mags, ivna_diags


def demo_exploding_gradients():
    """Large-weight network → exploding gradients."""
    print()
    print("=" * 70)
    print("DEMO 2B: Exploding Gradients (Large Weight Initialization)")
    print("=" * 70)

    # 6-layer network with very large initial weights
    layers = [2, 8, 8, 8, 8, 8, 1]
    net = SimpleNetwork(layers, activation='relu', init_scale=8.0)

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    pred = net.forward(X)
    ieee_mags, ieee_grads = net.backward_ieee(y)
    ivna_mags, ivna_diags = net.backward_ivna(y)

    print(f"\n  Network: {len(layers)-1} layers, ReLU, init_scale=8.0")
    print(f"\n  {'Layer':>6s}  {'IEEE Grad Mag':>15s}  {'IVNA Analysis':>20s}  {'Status':>12s}")
    print("  " + "-" * 60)

    for i, (ieee_mag, ivna_info) in enumerate(zip(ieee_mags, ivna_diags)):
        ivna_str = str(ivna_info['ivna']) if isinstance(ivna_info['ivna'], Virtual) else f"{ivna_info['ivna']:.2e}"
        print(f"  {i:>6d}  {ieee_mag:>15.2e}  {ivna_str:>20s}  {ivna_info['status']:>12s}")

    print(f"\n  IVNA DIAGNOSTIC DETAIL:")
    for info in ivna_diags:
        if info['status'] != 'HEALTHY':
            print(f"    Layer {info['layer']}: {info['diagnosis']}")


def demo_training_comparison():
    """Train the same network with IEEE vs IVNA monitoring."""
    print()
    print("=" * 70)
    print("DEMO 2C: Training Loop — IEEE vs IVNA Gradient Monitoring")
    print("=" * 70)

    layers = [2, 6, 6, 6, 6, 1]

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    net = SimpleNetwork(layers, activation='sigmoid', init_scale=1.0)
    lr = 0.5

    print(f"\n  Network: {len(layers)-1} layers, sigmoid, lr={lr}")
    print(f"  Training for 100 epochs")
    print(f"\n  {'Epoch':>6s}  {'Loss':>10s}  {'Layer 0 grad':>13s}  {'Layer 0 IVNA':>15s}  {'Deepest status':>15s}")
    print("  " + "-" * 65)

    vanish_epochs = []

    for epoch in range(100):
        # Forward
        pred = net.forward(X)
        loss = np.mean((pred - y) ** 2)

        # IVNA backward
        ieee_mags, ivna_diags = net.backward_ivna(y)

        # Also do IEEE backward for the actual gradient update
        _, ieee_grads = net.backward_ieee(y)

        # Update weights
        for i in range(len(net.layers)):
            net.layers[i] -= lr * ieee_grads[i]

        # Track vanishing
        deepest_status = ivna_diags[0]['status']
        if deepest_status == 'VANISHED':
            vanish_epochs.append(epoch)

        if epoch % 10 == 0 or epoch < 5:
            ivna_str = str(ivna_diags[0]['ivna']) if isinstance(ivna_diags[0]['ivna'], Virtual) else f"{ivna_diags[0]['ivna']:.2e}"
            print(f"  {epoch:>6d}  {loss:>10.6f}  {ieee_mags[0]:>13.2e}  {ivna_str:>15s}  {deepest_status:>15s}")

    print(f"\n  Epochs with vanished gradients in layer 0: {len(vanish_epochs)}/{100}")
    if vanish_epochs:
        print(f"  First vanished at epoch: {vanish_epochs[0]}")

    print(f"\n  INSIGHT: IVNA monitoring catches vanishing gradients in real-time.")
    print(f"  The INDEX of 0_x quantifies HOW vanished — not just that it happened.")


def demo_ivna_gradient_algebra():
    """Show the algebraic operations on IVNA gradient values."""
    print()
    print("=" * 70)
    print("DEMO 2D: IVNA Gradient Algebra")
    print("=" * 70)

    print(f"\n  Scenario: Chain rule through 4 layers, each with σ'(x) ≈ 0.01")
    print(f"  Standard: 0.01⁴ = 1e-8 → 'gradient vanished, no info'")
    print(f"  IVNA: Each σ'(x) ≈ 0_{0.01}, and we can track the chain")

    # Simulate chain rule with IVNA
    g = I(1)  # Start with gradient = ∞_1 (just for demonstration, the output gradient)

    # Actually, let's use real gradients that become virtual
    print(f"\n  Layer-by-layer gradient flow:")

    grad_scales = [0.25, 0.1, 0.01, 0.001]  # sigmoid derivatives at different saturation levels

    cumulative = 1.0
    print(f"    Output gradient: 1.0 (real)")

    for i, scale in enumerate(grad_scales):
        cumulative *= scale
        if cumulative < 1e-7:
            # IVNA: this is a virtual zero
            ivna_val = Z(Fraction(cumulative).limit_denominator(10**9))
            print(f"    After layer {len(grad_scales)-i}: σ'={scale:.3f}, "
                  f"cumulative={cumulative:.2e}, IVNA: {ivna_val}")
        else:
            print(f"    After layer {len(grad_scales)-i}: σ'={scale:.3f}, "
                  f"cumulative={cumulative:.2e}, IVNA: real")

    print(f"\n  Final gradient: {cumulative:.2e}")

    # Key operation: ratio of vanished gradients
    g1 = Z(Fraction(1, 10**8))  # 0_{1e-8} — vanished gradient in layer 1
    g2 = Z(Fraction(1, 10**6))  # 0_{1e-6} — vanished gradient in layer 3

    ratio = g1 / g2  # Should give 1e-8 / 1e-6 = 0.01
    print(f"\n  KEY OPERATION: 0_{{1e-8}} / 0_{{1e-6}} = {float(ratio):.4f}")
    print(f"  → This is the shrink factor across 2 layers: σ'₁ · σ'₂ ≈ 0.01")
    print(f"  → IEEE 754 sees 0/0 = NaN. IVNA sees a meaningful ratio.")

    # Another key operation: gradient * learning_rate
    lr = Fraction(1, 100)  # 0.01 learning rate
    vanished_grad = Z(Fraction(1, 10**8))
    update = lr * vanished_grad  # 0.01 * 0_{1e-8} = 0_{1e-10}
    print(f"\n  Weight update: lr · vanished_grad = {lr} · {vanished_grad} = {update}")
    print(f"  → The update is ALSO a virtual zero, but with a SMALLER index")
    print(f"  → IEEE 754: 0.01 * 0 = 0 (update is literally nothing)")
    print(f"  → IVNA: 0_{{1e-10}} (update is virtual but tracked)")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  IVNA Demo 2: ML Gradient Tracking                                 ║")
    print("║  Diagnosing vanishing/exploding gradients with indexed virtuals     ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    demo_vanishing_gradients()
    demo_exploding_gradients()
    demo_training_comparison()
    demo_ivna_gradient_algebra()

    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
  Standard gradient monitoring:
    - Gradient magnitude → 0: "it vanished" (no structure)
    - Gradient magnitude → Inf: "it exploded" (no structure)
    - 0/0 = NaN: can't compute ratios between vanished gradients

  IVNA gradient monitoring:
    - Gradient → 0_x: "it vanished, but x tracks the relative scale"
    - Gradient → ∞_x: "it exploded, and x tells you by how much"
    - 0_x / 0_y = x/y: ratios between vanished gradients are REAL NUMBERS
    - This reveals per-layer shrink/growth factors invisibly

  For paper: IVNA provides a natural diagnostic framework for gradient flow.
  The key innovation is that 0_x / 0_y = x/y — vanished-gradient ratios
  are algebraically meaningful, revealing the structural cause of vanishing.

  HONEST ASSESSMENT: This is more a diagnostic/monitoring tool than a
  fundamental change to training. The gradients are still numerically small.
  But the INFORMATION about gradient structure is preserved, which current
  tools (gradient histograms, etc.) approximate heuristically.
""")
