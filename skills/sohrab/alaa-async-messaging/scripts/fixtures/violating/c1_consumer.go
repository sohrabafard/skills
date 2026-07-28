package worker

// Violates C1: a consumer construction site with no prefetch anywhere in the file.

import "example.com/kit/mqkit"

func Start(c *mqkit.Client) error {
	return c.NewConsumer("entitlement.projector.work").Run()
}
