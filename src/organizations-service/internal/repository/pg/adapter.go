package pg

import (
	"database/sql"
	"organizations/internal/domain"
)

type Adapter struct {
	Client *sql.DB
}

func NewAdapter(db *sql.DB) *Adapter {
	return &Adapter{db}
}

func (a *Adapter) Save(organization domain.Organization) error {
	query := "INSERT INTO ORGANIZATIONS(ID,NAME,MAIN_COLOR) VALUES($1,$2,$3)"
	_, err := a.Client.Exec(query, organization.Id, organization.Name, organization.MainColor)
	if err != nil {
		return err
	}
	return nil
}
