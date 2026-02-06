const { isValidAge } = require("./pattern");

describe("isValidAge", () => {
  test("returns true for valid age", () => {
    expect(isValidAge(18)).toBe(true);
    expect(isValidAge(25)).toBe(true);
  });

  test("returns false for underage values", () => {
    expect(isValidAge(17)).toBe(false);
    expect(isValidAge(0)).toBe(false);
  });

  test("returns false for unrealistically high ages", () => {
    expect(isValidAge(121)).toBe(false);
  });

  test("returns false for non-numeric input", () => {
    expect(isValidAge("18")).toBe(false);
    expect(isValidAge(null)).toBe(false);
    expect(isValidAge(undefined)).toBe(false);
  });
});
