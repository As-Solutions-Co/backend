package repository

import "students/internal/domain"

type StudentRepo interface {
	Save(student domain.Student) (string, error)
	FindAll() ([]domain.Student, error)
	FindById(string) (domain.Student, error)
	Update(student domain.Student) (string, error)
	Delete(string) error
}
