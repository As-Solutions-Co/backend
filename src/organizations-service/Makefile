#build:
#	go mod tidy
#	GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -tags lambda.norpc -ldflags="-s -w" -trimpath -o bootstrap cmd/main.go
#	zip myFunction.zip bootstrap
#	aws lambda update-function-code --function-name go --zip-file fileb://myFunction.zip
