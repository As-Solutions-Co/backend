package application

import (
	"context"
	"math/rand"
	"organizations/internal/domain"
	"organizations/internal/ports"
	"time"
)

type Service struct {
	repository ports.Repository
}

func NewService(repository ports.Repository) *Service {
	return &Service{repository}
}

func (s Service) CreateOrganization(ctx context.Context, organizationIn domain.Organization) (any, error) {
	organizationIn.Id = int(time.Now().UnixMicro()) * rand.Intn(10000)
	err := s.repository.Save(ctx, organizationIn)
	if err != nil {
		return nil, err
	}
	return organizationIn, nil
}

func (s Service) GetOrganizationById(ctx context.Context, id string) (domain.Organization, error) {
	return s.repository.Find(ctx, id)
}

func (s Service) GetAllOrganizations(ctx context.Context) ([]domain.Organization, error) {
	return s.repository.FindAll(ctx)
}
