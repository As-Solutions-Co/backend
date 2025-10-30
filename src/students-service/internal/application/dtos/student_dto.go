package dtos

import (
	"students/internal/domain"
	"time"

	"github.com/go-playground/validator/v10"
)

type StudentCreateRequest struct {
	Document  string `json:"document" validate:"required,number"`
	FirstName string `json:"first_name" validate:"required"`
	LastName  string `json:"middle_name" validate:"required"`
	Email     string `json:"email" validate:"required,email"`
	Phone     string `json:"phone" validate:"required,numeric"`
}

type StudentUpdateRequest struct {
	Document  string  `json:"document" validate:"required,number"`
	FirstName *string `json:"first_name" validate:"omitempty"`
	LastName  *string `json:"last_name" validate:"omitempty"`
	Email     *string `json:"email" validate:"omitempty,email"`
	Phone     *string `json:"phone" validate:"omitempty,numeric"`
}
type StudentResponse struct {
	Id        string    `json:"id"`
	Document  string    `json:"document"`
	FirstName string    `json:"first_name"`
	LastName  string    `json:"middle_name"`
	Email     string    `json:"email"`
	Phone     string    `json:"phone"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

func (DTO StudentCreateRequest) ToDomain(v *validator.Validate) (domain.Student, error) {
	err := v.Struct(DTO)
	if err != nil {
		return domain.Student{}, err
	}
	return domain.Student{
		Document:  DTO.Document,
		FirstName: DTO.FirstName,
		LastName:  DTO.LastName,
		Email:     DTO.Email,
		Phone:     DTO.Phone,
	}, nil
}
