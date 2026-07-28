package worker

// Conforming: explicit prefetch at the construction site, a declared dead-letter
// target, and registry-conforming names.

import "example.com/kit/mqkit"

func Start(c *mqkit.Client) error {
	q := mqkit.QueueDecl{
		Name:        "notification.command.sms.send_pattern.v1",
		Prefetch:    32,
		Concurrency: 8,
		DLQDecl: mqkit.DeadLetter{
			Exchange:   "notification.commands.dlx",
			RoutingKey: "sms.send_pattern.v1.failed",
		},
	}
	return c.NewConsumer(q).Run()
}
