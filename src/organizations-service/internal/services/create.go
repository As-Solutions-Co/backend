package services

import (
	"math/rand"
	"organizations/internal/domain"
	"organizations/internal/repository"
	"time"
)

func CreateService(organizationIn domain.Organization, repo repository.IRepository) (any, error) {

	organizationIn.Id = int(time.Now().UnixMicro()) * rand.Intn(10000)
	err := repo.Save(organizationIn)
	if err != nil {
		return nil, err
	}
	return organizationIn, nil
}
