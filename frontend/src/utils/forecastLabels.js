// The backend always returns forecast points at these exact minute
// offsets (backend/predictor.py FORECAST_INTERVALS = [0, 30, 60, 120, 180]).
export function forecastMinutesLabel(minutes) {
  if (minutes === 0) return "NOW";
  if (minutes < 60) return `+${minutes} MIN`;
  const hours = minutes / 60;
  return `+${hours} HR`;
}
