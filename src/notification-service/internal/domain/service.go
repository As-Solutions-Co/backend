package domain

import "notifications/internal/ports"

type Service struct {
	notifier ports.Notifier
}

func NewService(notifier ports.Notifier) *Service {
	return &Service{notifier: notifier}
}

func (s *Service) SendNotification(message string) error { return s.notifier.SendNotification(message) }
