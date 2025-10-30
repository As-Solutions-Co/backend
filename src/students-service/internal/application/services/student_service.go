package services

import (
	"students/internal/application/dtos"
	"students/internal/domain"
	"students/internal/ports/repository"

	"github.com/go-playground/validator/v10"
	"github.com/google/uuid"
)

type StudentService struct {
	repo      repository.StudentRepo
	validator *validator.Validate
}

func NewStudentService(r repository.StudentRepo, v *validator.Validate) *StudentService {
	return &StudentService{repo: r, validator: v}
}

func (s *StudentService) Create(DTO dtos.StudentCreateRequest) (string, error) {
	student, err := DTO.ToDomain(s.validator)
	if err != nil {
		return "failed", err
	}
	studentId, err := s.repo.Save(student)
	if err != nil {
		return "", err
	}
	return studentId, nil
}

func (s *StudentService) GetAll() ([]domain.Student, error) {
	return s.repo.FindAll()
}

func (s *StudentService) GetById(id string) (domain.Student, error) {
	err := uuid.Validate(id)
	if err != nil {
		return domain.Student{}, err
	}
	return s.repo.FindById(id)
}
