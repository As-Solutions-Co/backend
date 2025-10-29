package main

import (
	"database/sql"
	"log"
	"organizations/internal/adapters/broker"
	"organizations/internal/application"
	"os"
	"time"

	"organizations/internal/adapters/handler"
	"organizations/internal/adapters/repository"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
	amqp "github.com/rabbitmq/amqp091-go"
)

var (
	pgClient *sql.DB
	rabbitCh *amqp.Channel
)

func init() {
	var err error
	connURI := os.Getenv("CONN_URI")
	if connURI == "" {
		log.Fatal("CONN_URI must be set")
	}
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
	rabbitConn, err := amqp.Dial(os.Getenv("RABBIT_MQ_URL"))
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %s", err)
	}
	rabbitCh, err = rabbitConn.Channel()
	if err != nil {
		log.Fatalf("Failed to open a channel: %s", err)
	}

}

func main() {
	defer rabbitCh.Close()
	defer pgClient.Close()
	pgRepo := repository.NewPostgresRepository(pgClient)
	rabbitBroker := broker.NewRabbitMQPublisher(rabbitCh)
	service := application.NewService(pgRepo, rabbitBroker)
	GinHandler := handler.NewGinHandler(*service)

	router := gin.Default()
	router.POST("/organizations", GinHandler.CreateOrganizationHandler)
	router.GET("/organizations", GinHandler.GetAllOrganizationsHandler)
	router.GET("/organizations/:id", GinHandler.GetOrganizationByIdHandler)
	//router.PUT("/organizations/:id",)

	if err := router.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
