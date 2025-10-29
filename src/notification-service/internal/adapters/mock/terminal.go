package mock

import "log"

type TerminalNotifier struct{}

func NewMockTerminalNotifier() *TerminalNotifier {
	return &TerminalNotifier{}
}
func (m *TerminalNotifier) SendNotification(message string) error {
	log.Println("Sending message:", message)
	return nil
}
