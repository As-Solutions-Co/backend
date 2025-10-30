-- +goose Up
-- +goose StatementBegin
CREATE TABLE STUDENTS
(
    ID         UUID PRIMARY KEY,
    DOCUMENT   VARCHAR   NOT NULL UNIQUE,
    FIRST_NAME VARCHAR   NOT NULL,
    LAST_NAME  VARCHAR   NOT NULL,
    EMAIL      VARCHAR   NOT NULL UNIQUE,
    PHONE      VARCHAR   NOT NULL,
    CREATED_AT TIMESTAMP NOT NULL,
    UPDATED_AT TIMESTAMP NOT NULL DEFAULT NOW()
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE STUDENTS;
-- +goose StatementEnd
