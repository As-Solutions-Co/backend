package domain

import (
	"time"
)

type Student struct {
	Id        string
	Document  string
	FirstName string
	LastName  string
	Email     string
	Phone     string
	CreatedAt time.Time
	UpdatedAt time.Time
}
