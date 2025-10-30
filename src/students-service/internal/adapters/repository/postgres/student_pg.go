package postgres

import (
	"database/sql"
	"errors"
	"fmt"
	"students/internal/domain"

	"github.com/google/uuid"
	"github.com/lib/pq"
)

type StudentPgRepository struct {
	db *sql.DB
}

func NewStudentPgRepository(db *sql.DB) *StudentPgRepository {
	return &StudentPgRepository{db: db}
}

func (r *StudentPgRepository) Save(s domain.Student) (string, error) {
	s.Id = uuid.New().String()
	query := `INSERT INTO STUDENTS(ID,DOCUMENT,FIRST_NAME,LAST_NAME,EMAIL,PHONE,CREATED_AT)
			  VALUES ($1,$2,$3,$4,$5,$6,NOW())`
	result, err := r.db.Exec(query, s.Id, s.Document, s.FirstName, s.LastName, s.Email, s.Phone)
	if err != nil {
		var pqErr *pq.Error
		if errors.As(err, &pqErr) {
			fmt.Printf("Código: %s\nMensaje: %s\nTabla: %s\nColumna: %s\nRestricción: %s\n",
				pqErr.Code, pqErr.Message, pqErr.Table, pqErr.Column, pqErr.Constraint)
			switch pqErr.Code {
			case "23505":
				return "", err
			case "23503":
				return "", err
			case "23514":
				return "", err
			default:
				return "", err
			}
		}
		fmt.Println(result)
	}
	return s.Id, nil
}

func (r *StudentPgRepository) FindAll() ([]domain.Student, error) {
	var students []domain.Student
	query := "SELECT ID,DOCUMENT,FIRST_NAME,LAST_NAME,EMAIL,PHONE,CREATED_AT,UPDATED_AT FROM STUDENTS"
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		student := domain.Student{}
		err = rows.Scan(
			&student.Id,
			&student.Document,
			&student.FirstName,
			&student.LastName,
			&student.Email,
			&student.Phone,
			&student.CreatedAt,
			&student.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		students = append(students, student)
	}
	return students, nil
}

func (r *StudentPgRepository) FindById(id string) (domain.Student, error) {
	query := "SELECT * FROM STUDENTS WHERE ID = $1"
	row := r.db.QueryRow(query, id)
	student := domain.Student{}
	err := row.Scan(
		&student.Id,
		&student.Document,
		&student.FirstName,
		&student.LastName,
		&student.Email,
		&student.Phone,
		&student.CreatedAt,
		&student.UpdatedAt,
	)
	if err != nil {
		return student, err
	}
	return student, nil
}

func (r *StudentPgRepository) Update(s domain.Student) (string, error) {
	//TODO implement me
	panic("implement me")
}

func (r *StudentPgRepository) Delete(id string) error {
	//TODO implement me
	panic("implement me")
}
