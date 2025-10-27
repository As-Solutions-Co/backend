package ports

import (
	"context"
	"organizations/internal/domain"
)

type Repository interface {
	Save(ctx context.Context, organization domain.Organization) error
	Find(ctx context.Context, id string) (domain.Organization, error)
	FindAll(ctx context.Context) ([]domain.Organization, error)
}
