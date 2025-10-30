package domain

import (
	"time"

	"github.com/go-playground/validator/v10"
)

type Guardian struct {
	Id        string    `json:"id" validate:"required,uuid4"`
	FirstName string    `json:"first_name" validate:"required"`
	LastName  string    `json:"last_name" validate:"required"`
	Email     string    `json:"email" validate:"required,email"`
	Phone     string    `json:"phone" validate:"required,number"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

func (g *Guardian) Validate() error {
	v := validator.New()
	return v.Struct(g)
}
