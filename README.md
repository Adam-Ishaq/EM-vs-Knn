# 🎯 Overview
Missing values are a pervasive challenge in metabolomics data, arising from technical limitations such as values below the limit of detection (LOD), ion suppression, or instrument variability.
The choice of imputation method can significantly impact downstream biological interpretations, yet systematic comparisons with proper statistical rigor are lacking.
This repository compares two imputation approaches:

**Expectation-Maximization (EM):** A probabilistic model-based approach assuming multivariate Gaussian distribution with regularization for high-dimensional metabolomics data

**K-Nearest Neighbors (KNN):** A non-parametric distance-based method that leverages similarity between samples

**Key Contributions:**

Complete mathematical derivation of EM algorithm for metabolomics
Rigorous missingness pattern analysis (Little's MCAR test, MAR/MNAR detection)
Comprehensive evaluation framework with multiple metrics
Statistical comparison using paired tests and bootstrapping
Biological validation through pathway preservation analysis
Fully reproducible computational pipeline

# ✨ Features
# 📊 Data Processing

mzML file parsing and peak detection
Cross-sample peak alignment
Multiple normalization strategies (PQN, TIC, median)
Quality control filtering

# 🔍 Missingness Analysis

Statistical characterization of missing patterns
Little's MCAR test implementation
MAR vs MNAR discrimination
Comprehensive visualization suite

# 🧮 EM Algorithm Implementation

Mathematical rigor: Full derivation from first principles
Regularization: Ridge penalty for numerical stability (Σ + λI)
Convergence diagnostics: Log-likelihood tracking
Optimization: Efficient handling of sparse data

# 📈 Evaluation Framework

Performance metrics: RMSE, MAE, Pearson/Spearman correlation
Statistical testing: Paired t-tests, Wilcoxon signed-rank tests
Cross-validation: K-fold and leave-one-out strategies
Biological validation: PCA preservation, pathway analysis

