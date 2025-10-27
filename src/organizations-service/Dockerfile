FROM golang:1.25.3-alpine AS builder
WORKDIR /build_stage
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go mod tidy
RUN CGO_ENABLED=0 go build -tags lambda.norpc -ldflags="-s -w" -o app cmd/api/main.go

FROM scratch
WORKDIR /app
COPY --from=builder /build_stage/app .
ENTRYPOINT ["./app"]
