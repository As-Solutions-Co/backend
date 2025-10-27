package repository

import (
	"context"
	"database/sql"
	"errors"
	"organizations/internal/domain"
)

type PostgresRepository struct {
	client *sql.DB
}

func NewPostgresRepository(client *sql.DB) PostgresRepository {
	return PostgresRepository{client}
}

func (r PostgresRepository) Save(ctx context.Context, organization domain.Organization) error {
	query := "INSERT INTO ORGANIZATIONS(ID,NAME,MAIN_COLOR) VALUES($1,$2,$3)"
	_, err := r.client.ExecContext(ctx, query, organization.Id, organization.Name, organization.MainColor)
	if err != nil {
		return err
	}
	return nil
}

func (r PostgresRepository) Find(ctx context.Context, id string) (domain.Organization, error) {
	var o domain.Organization
	query := "SELECT * FROM ORGANIZATIONS WHERE ID = $1"
	row := r.client.QueryRowContext(ctx, query, id)
	err := row.Scan(&o.Id, &o.Name, &o.MainColor)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return o, domain.OrganizationNotFoundError
		}
		return o, err
	}
	return o, nil
}

func (r PostgresRepository) FindAll(ctx context.Context) ([]domain.Organization, error) {
	var organizations []domain.Organization
	query := "SELECT * FROM ORGANIZATIONS"
	rows, err := r.client.QueryContext(ctx, query)
	if err != nil {
		return organizations, err
	}
	defer rows.Close()
	for rows.Next() {
		var o domain.Organization
		err := rows.Scan(&o.Id, &o.Name, &o.MainColor)
		if err != nil {
			return organizations, err
		}
		organizations = append(organizations, o)
	}
	return organizations, nil
}
