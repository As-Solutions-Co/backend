package repository

import "students/internal/domain"

type GuardianRepository interface {
	Save(*domain.Guardian) error
	FindAll() ([]*domain.Guardian, error)
	FindById(string) (*domain.Guardian, error)
	Update(*domain.Guardian) error
	Delete(string) error
}
