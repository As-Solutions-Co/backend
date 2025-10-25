package domain

type Organization struct {
	Id        interface{} `json:"id"`
	Name      string      `json:"name"`
	MainColor string      `json:"main_color"`
}
