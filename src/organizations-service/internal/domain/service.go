package domain

import (
	"context"
	"math/rand"
	"organizations/internal/ports"
	"time"
)

type Service struct {
	repo   ports.Repository
	broker ports.Broker
}

func NewService(r ports.Repository, b ports.Broker) *Service {
	return &Service{r, b}
}

func (s Service) Create(ctx context.Context, orgIn Organization) (any, error) {
	orgIn.Id = int(time.Now().UnixMicro()) * rand.Intn(10000)
	err := s.repo.Save(ctx, orgIn)
	if err != nil {
		return nil, err
	}
	return orgIn, nil
}

func (s Service) GetById(ctx context.Context, id string) (Organization, error) {
	org, err := s.repo.Find(ctx, id)
	if err != nil {
		return org, err
	}
	err = s.broker.Publish("hello", "Hi from GetById organizations service")
	if err != nil {
		return org, err
	}
	return org, nil
}

func (s Service) GetAllOrganizations(ctx context.Context) ([]Organization, error) {
	return s.repo.FindAll(ctx)
}

//
//func (s Service) Update(ctx context.Context, id string, orgIn domain.OrganizationCreate) (any, error) {
//	var fieldsToUpdate []string
//
//}

func (s Service) Delete(ctx context.Context, id string) error {
	return s.repo.Delete(ctx, id)
}
