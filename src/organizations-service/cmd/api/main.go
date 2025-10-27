package main

import (
	"database/sql"
	"log"
	"os"
	"time"

	"organizations/internal/adapters/handler"
	"organizations/internal/adapters/repository"
	"organizations/internal/application"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

var pgClient *sql.DB

func init() {
	var err error
	connURI := os.Getenv("CONN_URI")
	if connURI == "" {
		log.Fatal("CONN_URI must be set")
	}
	log.Printf("Attempting to connect with URI: %s\n", connURI)
	pgClient, err = sql.Open("postgres", connURI)
	if err != nil {
		log.Fatal(err)
	}
	pgClient.SetConnMaxLifetime(30 * time.Second)
	pgClient.SetConnMaxIdleTime(5 * time.Second)
	pgClient.SetMaxOpenConns(10)
	pgClient.SetMaxIdleConns(5)

	err = pgClient.Ping()
	if err != nil {
		log.Fatalf("Initial database ping failed: %v", err)
	}

	log.Println("Database connection successful and pool configured.")
}

func main() {
	repo := repository.NewPostgresRepository(pgClient)
	service := application.NewService(repo)
	GinHandler := handler.NewGinHandler(*service)

	router := gin.Default()
	router.POST("/organizations", GinHandler.CreateOrganizationHandler)
	router.GET("/organizations", GinHandler.GetAllOrganizationsHandler)
	router.GET("/organizations/:id", GinHandler.GetOrganizationByIdHandler)

	if err := router.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
