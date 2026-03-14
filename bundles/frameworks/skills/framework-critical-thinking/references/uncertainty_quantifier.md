# Uncertainty Quantifier

## Purpose

The Uncertainty Quantifier calibrates confidence scores to match actual accuracy, ensuring that stated confidence levels are reliable indicators of correctness.

## Confidence Calibration

### The Calibration Problem

Models often exhibit:
- **Overconfidence:** Stating high confidence for incorrect answers
- **Underconfidence:** Stating low confidence for correct answers

### Calibration Methods

#### 1. Temperature Scaling

```python
class TemperatureScaler:
    def __init__(self):
        self.temperature = 1.0

    def fit(self, confidences, accuracies):
        """Learn optimal temperature on validation set."""
        def nll_loss(T):
            scaled = self.scale_confidences(confidences, T)
            return -np.mean(
                accuracies * np.log(scaled) +
                (1 - accuracies) * np.log(1 - scaled)
            )

        self.temperature = minimize(nll_loss, x0=1.0).x[0]

    def calibrate(self, confidence):
        """Apply temperature scaling."""
        return self.scale_confidences(confidence, self.temperature)

    def scale_confidences(self, confidences, temperature):
        return 1 / (1 + np.exp(-np.log(confidences / (1 - confidences)) / temperature))
```

#### 2. Platt Scaling

```python
class PlattScaler:
    def __init__(self):
        self.a = 1.0
        self.b = 0.0

    def fit(self, confidences, accuracies):
        """Fit sigmoid parameters."""
        from scipy.optimize import minimize

        def loss(params):
            a, b = params
            calibrated = 1 / (1 + np.exp(-(a * confidences + b)))
            return -np.mean(
                accuracies * np.log(calibrated + 1e-10) +
                (1 - accuracies) * np.log(1 - calibrated + 1e-10)
            )

        result = minimize(loss, x0=[1.0, 0.0])
        self.a, self.b = result.x

    def calibrate(self, confidence):
        """Apply Platt scaling."""
        return 1 / (1 + np.exp(-(self.a * confidence + self.b)))
```

#### 3. Isotonic Regression

```python
class IsotonicCalibrator:
    def __init__(self):
        from sklearn.isotonic import IsotonicRegression
        self.iso = IsotonicRegression(out_of_bounds='clip')

    def fit(self, confidences, accuracies):
        """Fit isotonic regression."""
        self.iso.fit(confidences, accuracies)

    def calibrate(self, confidence):
        """Apply isotonic calibration."""
        return self.iso.predict([confidence])[0]
```

## Calibration Metrics

### Expected Calibration Error (ECE)

```python
def expected_calibration_error(confidences, predictions, labels, n_bins=10):
    """Calculate ECE - lower is better."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    for lower, upper in zip(bin_lowers, bin_uppers):
        in_bin = (confidences > lower) & (confidences <= upper)
        prop_in_bin = in_bin.mean()

        if prop_in_bin > 0:
            accuracy_in_bin = (predictions[in_bin] == labels[in_bin]).mean()
            avg_confidence_in_bin = confidences[in_bin].mean()
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

    return ece
```

### Maximum Calibration Error (MCE)

```python
def maximum_calibration_error(confidences, predictions, labels, n_bins=10):
    """Calculate MCE - worst-case calibration error."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    errors = []

    for i in range(n_bins):
        lower, upper = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (confidences > lower) & (confidences <= upper)

        if in_bin.sum() > 0:
            accuracy = (predictions[in_bin] == labels[in_bin]).mean()
            confidence = confidences[in_bin].mean()
            errors.append(np.abs(confidence - accuracy))

    return max(errors) if errors else 0.0
```

### Brier Score

```python
def brier_score(confidences, outcomes):
    """Calculate Brier score - lower is better."""
    return np.mean((confidences - outcomes) ** 2)
```

## Confidence Intervals

```python
class ConfidenceIntervalEstimator:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level

    def estimate_interval(self, predictions, variances):
        """Estimate confidence intervals."""
        from scipy import stats

        z_score = stats.norm.ppf((1 + self.confidence_level) / 2)

        lower = predictions - z_score * np.sqrt(variances)
        upper = predictions + z_score * np.sqrt(variances)

        return {'lower': lower, 'upper': upper, 'confidence': self.confidence_level}

    def monte_carlo_dropout(self, model, input_data, n_samples=100):
        """Estimate uncertainty using MC dropout."""
        predictions = []
        model.train()  # Enable dropout

        for _ in range(n_samples):
            pred = model(input_data)
            predictions.append(pred)

        predictions = torch.stack(predictions)
        mean = predictions.mean(dim=0)
        variance = predictions.var(dim=0)

        return {'mean': mean, 'variance': variance}
```

## Usage Example

```python
# Collect calibration data
confidences = []
accuracies = []

for task in validation_set:
    confidence, prediction, actual = agent.solve_with_confidence(task)
    confidences.append(confidence)
    accuracies.append(prediction == actual)

# Fit calibrator
calibrator = TemperatureScaler()
calibrator.fit(confidences, accuracies)

# Use calibrated confidence
raw_confidence = agent.get_confidence(new_task)
calibrated = calibrator.calibrate(raw_confidence)

print(f"Raw: {raw_confidence:.2f}, Calibrated: {calibrated:.2f}")
```

## Best Practices

1. **Use held-out calibration set** - Don't calibrate on training data
2. **Monitor ECE regularly** - Recalibrate if drift detected
3. **Consider task-specific calibration** - Different tasks may need different calibrators
4. **Report uncertainty** - Always provide confidence intervals, not just point estimates

---

**Sources:**
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599)
