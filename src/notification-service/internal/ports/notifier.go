package ports

type Notifier interface {
	SendNotification(message string) error
}
