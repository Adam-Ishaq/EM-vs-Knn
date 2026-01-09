"""
Utility functions for the metabolomics imputation project.
"""

import yaml
import logging
import os
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Parameters
    ----------
    config_path : str
        Path to the configuration file
        
    Returns
    -------
    dict
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """
    Set up logging configuration.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
        
    Returns
    -------
    logging.Logger
        Configured logger
    """
    log_dir = Path(config['paths']['logs'])
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f"metabolomics_imputation_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")
    return logger


def create_directories(config: Dict[str, Any]) -> None:
    """
    Create all necessary directories from config.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
    """
    for path_name, path_value in config['paths'].items():
        Path(path_value).mkdir(parents=True, exist_ok=True)


def save_results(data: Union[pd.DataFrame, np.ndarray],
                filename: str,
                config: Dict[str, Any],
                subdirectory: str = 'results') -> None:
    """
    Save results to file.
    
    Parameters
    ----------
    data : pd.DataFrame or np.ndarray
        Data to save
    filename : str
        Output filename
    config : dict
        Configuration dictionary
    subdirectory : str
        Subdirectory within results path
    """
    output_dir = Path(config['paths'][subdirectory])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / filename
    
    if isinstance(data, pd.DataFrame):
        if filename.endswith('.csv'):
            data.to_csv(output_path, index=True)
        elif filename.endswith('.xlsx'):
            data.to_excel(output_path, index=True)
        else:
            data.to_pickle(output_path)
    elif isinstance(data, np.ndarray):
        np.save(output_path, data)
    
    logging.info(f"Results saved to {output_path}")


def set_random_seed(seed: Optional[int] = None) -> None:
    """
    Set random seed for reproducibility.
    
    Parameters
    ----------
    seed : int, optional
        Random seed value
    """
    if seed is not None:
        np.random.seed(seed)
        import random
        random.seed(seed)
        logging.info(f"Random seed set to {seed}")


def get_sample_info(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a DataFrame with sample information.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
        
    Returns
    -------
    pd.DataFrame
        Sample information
    """
    samples = config['dataset']['samples']
    
    sample_info = []
    for group, count in samples.items():
        for i in range(count):
            sample_info.append({
                'sample_id': f"{group}_{i+1}",
                'group': group,
                'color': config['visualization']['colors'].get(group, '#999999')
            })
    
    return pd.DataFrame(sample_info)


def calculate_missing_percentage(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate percentage of missing values per feature and sample.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input data matrix
        
    Returns
    -------
    pd.DataFrame
        Missing value statistics
    """
    missing_stats = pd.DataFrame({
        'feature': data.columns,
        'n_missing': data.isnull().sum().values,
        'pct_missing': (data.isnull().sum() / len(data) * 100).values
    })
    
    missing_stats = missing_stats.sort_values('pct_missing', ascending=False)
    
    return missing_stats


def validate_data(data: pd.DataFrame, 
                 config: Dict[str, Any]) -> tuple[bool, list]:
    """
    Validate input data against configuration requirements.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input data
    config : dict
        Configuration dictionary
        
    Returns
    -------
    tuple
        (is_valid, list of error messages)
    """
    errors = []
    
    # Check number of samples
    expected_samples = sum(config['dataset']['samples'].values())
    if len(data) != expected_samples:
        errors.append(
            f"Expected {expected_samples} samples, got {len(data)}"
        )
    
    # Check for completely empty features
    empty_features = data.columns[data.isnull().all()]
    if len(empty_features) > 0:
        errors.append(
            f"Found {len(empty_features)} completely empty features"
        )
    
    # Check for completely empty samples
    empty_samples = data.index[data.isnull().all(axis=1)]
    if len(empty_samples) > 0:
        errors.append(
            f"Found {len(empty_samples)} completely empty samples"
        )
    
    is_valid = len(errors) == 0
    
    return is_valid, errors


def generate_report_summary(results: Dict[str, Any],
                           config: Dict[str, Any]) -> str:
    """
    Generate a text summary of analysis results.
    
    Parameters
    ----------
    results : dict
        Analysis results
    config : dict
        Configuration dictionary
        
    Returns
    -------
    str
        Formatted report summary
    """
    summary = []
    summary.append("=" * 80)
    summary.append("METABOLOMICS IMPUTATION ANALYSIS SUMMARY")
    summary.append("=" * 80)
    summary.append(f"\nProject: {config['project']['name']}")
    summary.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"\nDataset: {config['dataset']['name']}")
    summary.append(f"Total samples: {config['dataset']['total_files']}")
    summary.append("\n" + "-" * 80)
    
    for method, metrics in results.items():
        summary.append(f"\n{method.upper()} Results:")
        for metric_name, metric_value in metrics.items():
            summary.append(f"  {metric_name}: {metric_value:.4f}")
    
    summary.append("\n" + "=" * 80)
    
    return "\n".join(summary)


def export_session_info(config: Dict[str, Any], 
                       output_path: Optional[str] = None) -> None:
    """
    Export session information for reproducibility.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
    output_path : str, optional
        Output file path
    """
    import sys
    import platform
    
    session_info = {
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'platform': platform.platform(),
        'config': config
    }
    
    if output_path is None:
        output_path = Path(config['paths']['results']) / 'session_info.yaml'
    
    with open(output_path, 'w') as f:
        yaml.dump(session_info, f, default_flow_style=False)
    
    logging.info(f"Session info saved to {output_path}")
