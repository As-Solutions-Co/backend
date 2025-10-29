FROM golang:1.25.3-alpine AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go mod tidy
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o app cmd/rabbitmq/main.go

FROM scratch
WORKDIR /app
COPY --from=builder /build/app .
ENTRYPOINT ["./app"]