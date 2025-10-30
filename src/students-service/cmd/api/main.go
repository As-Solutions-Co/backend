package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"students/internal/adapters/repository/postgres"
	"students/internal/application/services"
	"time"

	"github.com/go-playground/validator/v10"
	_ "github.com/lib/pq"
)

func main() {
	startTime := time.Now()
	dbConn := os.Getenv("POSTGRES_URI")
	dbClient, err := sql.Open("postgres", dbConn)
	if err != nil {
		log.Fatal(err)
	}
	err = dbClient.Ping()
	if err != nil {
		log.Fatal(err)
	}
	v := validator.New()
	repo := postgres.NewStudentPgRepository(dbClient)
	service := services.NewStudentService(repo, v)
	//mock := dtos.StudentCreateDTO{
	//	Document:  "12345678",
	//	FirstName: "Juan",
	//	LastName:  "Smith",
	//	Email:     "juandiegar2003@gmail.com",
	//	Phone:     "+123454333",
	//}
	//id, err := service.Create(mock)
	//if err != nil {
	//	log.Println(err, time.Since(startTime))
	//	return
	//}
	//fmt.Println(id)
	data, err := service.GetById("4185a229-a5f4-4364-b501-8823f00f878e")
	if err != nil {
		log.Fatal(err)

	}
	fmt.Println("All Students:", data)
	fmt.Println("Total time:", time.Since(startTime))
}
