package ports

import (
	"context"
	"organizations/internal/domain"
)

type Repository interface {
	Save(ctx context.Context, organization domain.Organization) error
	Find(ctx context.Context, id string) (domain.Organization, error)
	FindAll(ctx context.Context) ([]domain.Organization, error)
	Update(ctx context.Context, updates map[string]string) error
	Delete(ctx context.Context, id string) error
}
