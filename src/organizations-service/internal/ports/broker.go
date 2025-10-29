package ports

type Broker interface {
	Publish(queue string, message string) error
}
