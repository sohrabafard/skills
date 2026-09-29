## Reproducing a quota condition locally

The failure this skill cares most about needs a recipe, or nobody exercises it.

- **Unit, any engine.** Inject a store double whose `put` fires an abort carrying
  `new DOMException('…', 'QuotaExceededError')`. Exercises the classification and the ladder without cost;
  this is the version that runs on every commit.
- **Playwright, Chromium.** Write increasingly large records into a throwaway store until the transaction
  aborts, then assert the error name and that the cleanup ladder ran. Slow — it belongs in the smoke lane.
- **Real device.** Fill the disk until the browser is under pressure. Manual, in the iOS and low-end
  Android lanes.

The unit form proves the branch; the Playwright form proves the engine raises what the branch expects.
Neither substitutes for the other.
