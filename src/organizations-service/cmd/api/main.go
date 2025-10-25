package main

import (
	"database/sql"
	"log"
	"net/http"
	"organizations/internal/domain"
	"organizations/internal/repository/pg"
	"organizations/internal/services"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

func main() {
	dbUri := "postgres://postgres:admin@172.17.0.2:5432/golang?sslmode=disable"
	db, err := sql.Open("postgres", dbUri)
	if err != nil {
		log.Fatalln(err)
	}
	err = db.Ping()
	if err != nil {
		log.Fatalln(err)
	}
	db.SetMaxOpenConns(60)

	router := gin.Default()
	router.POST("/organization", func(c *gin.Context) {
		var organizationIn domain.Organization
		if err := c.BindJSON(&organizationIn); err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{
				"message": "Invalid body",
			})
			return
		}
		id, err := services.CreateService(organizationIn, pg.NewAdapter(db))
		if err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{
				"message": err.Error(),
			})
			return
		}
		c.IndentedJSON(http.StatusOK, gin.H{
			"data": id,
		})
	})

	err = router.Run()
	if err != nil {
		log.Fatal(err)
	}
}
