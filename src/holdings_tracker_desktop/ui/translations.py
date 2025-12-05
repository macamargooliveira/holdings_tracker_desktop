current_lang = "pt_BR"

TRANSLATIONS = {
    "en": {
        "actions": "Actions",
        "add": "Add",
        "asset_events": "Asset Events",
        "asset_ticker_history": "Ticker Changes",
        "asset_types": "Asset Types",
        "asset": "Asset",
        "assets": "Assets",
        "basics": "Basic Registrations",
        "broker_notes": "Broker Notes",
        "broker": "Broker",
        "brokers": "Brokers",
        "countries": "Countries",
        "country": "Country",
        "currencies": "Currencies",
        "date": "Date",
        "delete": "Delete",
        "edit": "Edit",
        "fees": "Fees",
        "id": "ID",
        "languages": "Languages",
        "name": "Name",
        "operation": "Op.",
        "price": "Price",
        "quantity": "Qty.",
        "taxes": "Taxes",
        "total_value": "Total",
        "year": "Year"
    },

    "pt_BR": {
        "actions": "Ações",
        "add": "Incluir",
        "asset_events": "Eventos de Ativo",
        "asset_ticker_history": "Alterações de Ticker",
        "asset_types": "Tipos de Ativo",
        "asset": "Ativo",
        "assets": "Ativos",
        "basics": "Cadastros Básicos",
        "broker_notes": "Notas de Corretagem",
        "broker": "Corretora",
        "brokers": "Corretoras",
        "countries": "Países",
        "country": "País",
        "currencies": "Moedas",
        "date": "Data",
        "delete": "Excluir",
        "edit": "Editar",
        "fees": "Taxas",
        "id": "Código",
        "languages": "Idiomas",
        "name": "Nome",
        "operation": "Op.",
        "price": "Preço",
        "quantity": "Qtde.",
        "taxes": "IR",
        "total_value": "Total",
        "year": "Ano"
    }
}

def t(key: str) -> str:
    """Simple translation helper."""
    lang = TRANSLATIONS.get(current_lang, {})
    return lang.get(key, key)
