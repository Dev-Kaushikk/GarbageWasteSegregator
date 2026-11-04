/**
 * Garbage Waste Segregator Frontend - Formatted Number Utility
 *
 * Number formatting helpers for clean display.
 */

export const formatNumber = (num, decimals = 4) => {
  if (typeof num !== 'number') return '-';
  return num.toFixed(decimals);
};

export const formatPercentage = (num) => {
  const percentage = (num * 100).toFixed(2);
  return `${percentage}%`;
};

export const formatConfidence = (confidence) => {
  return `${Number(confidence).toFixed(3)}`;
};

export const formatArea = (area) => {
  return `${Number(area).toFixed(3)}`;
};

// Format large numbers with K/M suffixes
export const formatCompact = (num) => {
  if (Math.abs(num) >= 1_000_000) {
    return `${(num / 1_000_000).toFixed(1)}M`;
  }
  if (Math.abs(num) >= 1_000) {
    return `${(num / 1_000).toFixed(1)}K`;
  }
  return num.toFixed(0);
};

export default {
  formatNumber,
  formatPercentage,
  formatConfidence,
  formatArea,
  formatCompact,
};
