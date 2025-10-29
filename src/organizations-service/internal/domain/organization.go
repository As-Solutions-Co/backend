package domain

import (
	"github.com/go-playground/validator/v10"
)

type Organization struct {
	Id        interface{} `json:"id"`
	Name      string      `json:"name" validate:"required"`
	MainColor string      `json:"main_color" validate:"required"`
}
type OrganizationCreate struct {
	Name      string `json:"name"`
	MainColor string `json:"main_color"`
}

func (o Organization) Validate() error {
	v := validator.New()
	return v.Struct(o)
}
