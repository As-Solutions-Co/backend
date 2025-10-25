package repository

import "organizations/internal/domain"

type IRepository interface {
	Save(organization domain.Organization) error
}
