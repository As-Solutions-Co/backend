package repository

import "students/internal/domain"

type EnrollmentRepository interface {
	Save(*domain.Enrollment) error
	FindAll() ([]domain.Enrollment, error)
	FindById(string) (*domain.Enrollment, error)
	Update(*domain.Enrollment) error
	Delete(string) error
}
