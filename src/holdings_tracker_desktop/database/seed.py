from holdings_tracker_desktop.models import Country, Currency, AssetType, AssetSector, Broker

def run_initial_seeds(session):

    countries = [
        Country(name="Brasil"),
        Country(name="United States")
    ]
    session.add_all(countries)
    session.flush()

    brasil = next(c for c in countries if c.name == "Brasil")
    usa = next(c for c in countries if c.name == "United States")

    currencies = [
        Currency(code="BRL", name="Real Brasileiro", symbol="R$"),
        Currency(code="USD", name="United States Dollar", symbol="$")
    ]
    session.add_all(currencies)

    asset_types = [
        AssetType(name="Ação", country_id=brasil.id),
        AssetType(name="Fiagro", country_id=brasil.id),
        AssetType(name="FI-Infra", country_id=brasil.id),
        AssetType(name="FII", country_id=brasil.id),
        AssetType(name="Reit", country_id=usa.id),
        AssetType(name="Stock", country_id=usa.id)
    ]
    session.add_all(asset_types)
    session.flush()

    fii = next(a for a in asset_types if a.name == "FII")

    asset_sectors = [
        AssetSector(name="Híbridos", asset_type_id=fii.id),
        AssetSector(name="Lajes Comerciais", asset_type_id=fii.id),
        AssetSector(name="Logísticos", asset_type_id=fii.id),
        AssetSector(name="Recebíveis Imobiliários", asset_type_id=fii.id),
        AssetSector(name="Shoppings", asset_type_id=fii.id)
    ]
    session.add_all(asset_sectors)

    brokers = [
        Broker(name="BB-BI S.A.", country_id=brasil.id)
    ]
    session.add_all(brokers)
