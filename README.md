# signal-vs-noise

Understanding how information behaves when it starts to degrade.

🔗 Repository: https://github.com/cherikakaushal/signal-vs-noise

---

## Overview

Real-world systems rarely operate on perfect data.

This project explores how **information changes under different types of distortion** — not just whether it is correct, but whether it still *means the same thing*.

Instead of focusing only on accuracy, the goal is to study:
- how meaning degrades  
- how different failures affect systems differently  
- when a system actually breaks  

---

## Experiments

### 1. Noise Injection
Random noise added to text  
→ gradual degradation in meaning  

📄 Code: [exp1_noise.py](experiments/exp1_noise.py)  
📊 Output: [noise_similarity.png](visuals/noise_similarity.png)

---

### 2. Missing Context
Important words removed  
→ sharp loss of meaning  

📄 Code: [exp2_missing.py](experiments/exp2_missing.py)  
📊 Output: [missing_context.png](visuals/missing_context.png)

---

### 3. Bias Injection
Systematic distortion introduced  
→ meaning shifts without fully breaking  

📄 Code: [exp3_bias.py](experiments/exp3_bias.py)  
📊 Output: [bias_effect.png](visuals/bias_effect.png)

---

### 4. Combined Distortion
Noise + missing + bias together  
→ uneven system breakdown  

📄 Code: [exp4_combined.py](experiments/exp4_combined.py)  
📊 Output: [system_breakdown.png](visuals/system_breakdown.png)

---

## Blogs

- [What happens when signal becomes noise?](blogs/01-signal-vs-noise.md)
- [What happens when context is missing?](blogs/02-missing-context.md)
- [How bias distorts information](blogs/03-bias-distortion.md)
- [When does a system actually break?](blogs/04-system-breakdown.md)

---

## Key Insights

- Not all distortions are equal  
- Missing context damages systems more than random noise  
- Bias reshapes meaning without obvious failure  
- Systems do not fail uniformly — some inputs remain stable while others collapse  

---

## Visual Results

### Noise Impact
![Noise](visuals/noise_similarity.png)

### Missing Context
![Missing](visuals/missing_context.png)

### Bias Effect
![Bias](visuals/bias_effect.png)

### System Breakdown
![Breakdown](visuals/system_breakdown.png)

---


---

## Why this project

Most projects focus on building models.

This project focuses on understanding **how systems behave when things go wrong**.

---

## Next Direction

Extending this into:
- interactive simulations  
- real-time system behavior tracking  
- visualization dashboards  
