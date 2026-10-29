import { defineConfig } from "vitest/config";

// Release/restore archives under tmp contain historical test copies. Only the
// active product sources belong in the current frontend regression count.
export default defineConfig({
  test: { include: ["web/src/**/*.test.{ts,tsx}", "middleware.test.ts"] },
});
