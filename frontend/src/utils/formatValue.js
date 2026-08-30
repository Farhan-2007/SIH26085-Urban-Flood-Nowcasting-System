// Guards every numeric readout on the dashboard against the API returning
// null, undefined, or a non-numeric value — displays "N/A" instead of
// letting React render "NaN"/"undefined"/"null" to the screen.
export function formatNumber(value, { decimals = 0, suffix = "" } = {}) {
  if (value === null || value === undefined) return "N/A";
  const num = Number(value);
  if (Number.isNaN(num)) return "N/A";
  return `${num.toFixed(decimals)}${suffix}`;
}

// Formats a 0-1 fraction as a percentage string, guarding invalid input.
export function formatPercent(fraction, decimals = 0) {
  if (fraction === null || fraction === undefined) return "N/A";
  const num = Number(fraction);
  if (Number.isNaN(num)) return "N/A";
  return `${(num * 100).toFixed(decimals)}%`;
}

export function isValidNumber(value) {
  return value !== null && value !== undefined && !Number.isNaN(Number(value));
}
