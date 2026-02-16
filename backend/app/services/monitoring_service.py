from __future__ import annotations

import math

import numpy as np


class MonitoringService:
    def calculate_psi(self, expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
        breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        if len(breakpoints) < 3:
            return 0.0

        expected_percents = np.histogram(expected, bins=breakpoints)[0] / len(expected)
        actual_percents = np.histogram(actual, bins=breakpoints)[0] / len(actual)

        expected_percents = np.where(expected_percents == 0, 1e-4, expected_percents)
        actual_percents = np.where(actual_percents == 0, 1e-4, actual_percents)

        return float(np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents)))

    def ks_test(self, reference: np.ndarray, current: np.ndarray, alpha: float = 0.05) -> tuple[bool, float, float]:
        ref_sorted = np.sort(reference)
        cur_sorted = np.sort(current)

        data_all = np.concatenate([ref_sorted, cur_sorted])
        cdf_ref = np.searchsorted(ref_sorted, data_all, side="right") / len(ref_sorted)
        cdf_cur = np.searchsorted(cur_sorted, data_all, side="right") / len(cur_sorted)
        statistic = np.max(np.abs(cdf_ref - cdf_cur))

        n1 = len(ref_sorted)
        n2 = len(cur_sorted)
        ne = n1 * n2 / (n1 + n2)
        p_value = min(1.0, 2 * math.exp(-2 * ne * statistic**2))
        return p_value < alpha, float(statistic), float(p_value)


monitoring_service = MonitoringService()
