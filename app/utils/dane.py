from httpx import HTTPError, get

from app.models.organization_model import OrganizationDane

DANE_URL = "https://sise.dane.gov.co/servicios/sise-2/tramites-consulta-btn.php"


def get_legal_information_from_dane(dane_code: str) -> OrganizationDane | None:
    try:
        dane_response = get(DANE_URL, params={"codigo": dane_code})
        dane_response.raise_for_status()

        response_json = dane_response.json()

        if "data" in response_json and response_json["data"]:
            dane_data = response_json["data"][0]

            organization_data = {
                "dane_code": dane_code,
                "name": dane_data.get("NOMBRE_INSTITUCION"),
                "latitude": dane_data.get("LATITUD"),
                "longitude": dane_data.get("LONGITUD"),
                "address": dane_data.get("DIRECCION"),
            }
            return OrganizationDane(**organization_data)

    except HTTPError:
        return None
