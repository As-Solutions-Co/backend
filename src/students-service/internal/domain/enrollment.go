package domain

import "github.com/go-playground/validator/v10"

type Enrollment struct {
	Id         string `json:"id" validate:"required,uuid4"`
	StudentId  string `json:"student_id" validate:"required,uuid4"`
	SchoolYear int    `json:"school_year" validate:"required,numeric"`
	GradeLevel string `json:"grade_level" validate:"required,numeric"`
	EnrolledAt int64  `json:"enrolled_at" validate:"required,numeric"`
	Status     string `json:"status" validate:"required oneOf=active retired"`
}

func (e *Enrollment) Validate() error {
	v := validator.New()
	return v.Struct(e)
}
