function isValidAge(age) {
  if (typeof age !== "number") return false;
  if (age < 18) return false;
  if (age > 120) return false;
  return true;
}

module.exports = { isValidAge };
