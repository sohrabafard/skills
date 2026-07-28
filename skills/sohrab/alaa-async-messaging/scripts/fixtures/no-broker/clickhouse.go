package analytics

// No broker lane: this service reads a ClickHouse lane and declares nothing on
// any broker. The gate must report exit 2 rather than a pass.

func Query(sql string) error { return nil }
