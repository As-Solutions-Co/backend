package handler

import (
	"context"
	"errors"
	"net/http"
	"organizations/internal/application"
	"organizations/internal/domain"
	"time"

	"github.com/gin-gonic/gin"
)

type GinHandler struct {
	service application.Service
}

func NewGinHandler(service application.Service) *GinHandler {
	return &GinHandler{service}
}

func (h *GinHandler) CreateOrganizationHandler(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), time.Second*3)
	defer cancel()
	var organizationIn domain.Organization
	if err := c.BindJSON(&organizationIn); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := organizationIn.Validate(); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	newOrganization, err := h.service.Create(ctx, organizationIn)
	if err != nil {
		if errors.Is(err, context.DeadlineExceeded) {
			c.JSON(http.StatusGatewayTimeout, gin.H{"error": "request timed out"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
		return
	}
	c.JSON(http.StatusCreated, newOrganization)
}

func (h *GinHandler) GetOrganizationByIdHandler(c *gin.Context) {
	id := c.Param("id")
	ctx, cancel := context.WithTimeout(c.Request.Context(), time.Second*3)
	defer cancel()
	organization, err := h.service.GetById(ctx, id)
	if err != nil {
		if errors.Is(err, context.DeadlineExceeded) {
			c.JSON(http.StatusGatewayTimeout, gin.H{"error": "request timed out"})
			return
		}
		if errors.Is(err, domain.OrganizationNotFoundError) {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
		return
	}
	c.JSON(http.StatusOK, organization)
}

func (h *GinHandler) GetAllOrganizationsHandler(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), time.Second*3)
	defer cancel()
	organizations, err := h.service.GetAllOrganizations(ctx)
	if err != nil {
		if errors.Is(err, context.DeadlineExceeded) {
			c.JSON(http.StatusGatewayTimeout, gin.H{"error": "request timed out"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
		return
	}
	c.JSON(http.StatusOK, organizations)
}
