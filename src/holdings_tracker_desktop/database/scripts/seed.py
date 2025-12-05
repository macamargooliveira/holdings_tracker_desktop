from holdings_tracker_desktop.database.database import SessionLocal
from holdings_tracker_desktop.models import Country, Currency, AssetType, Broker

def run_seeds():
    db = SessionLocal()

    try:
        countries = [
            Country(name="Brasil"),
            Country(name="United States")
        ]
        db.add_all(countries)

        currencies = [
            Currency(code="BRL", name="Real Brasileiro", symbol="R$"),
            Currency(code="USD", name="United States Dollar", symbol="$")
        ]
        db.add_all(currencies)

        asset_types = [
            AssetType(name="Ação", country_id=1),
            AssetType(name="Fiagro", country_id=1),
            AssetType(name="FI-Infra", country_id=1),
            AssetType(name="FII", country_id=1),
            AssetType(name="Reit", country_id=2),
            AssetType(name="Stock", country_id=2)
        ]
        db.add_all(asset_types)

        brokers = [
            Broker(name="BB-BI S.A.", country_id=1)
        ]
        db.add_all(brokers)

        db.commit()
        print("Seeds inserted successfully!")

    except Exception as e:
        db.rollback()
        print("Seed error:", e)

    finally:
        db.close()

if __name__ == "__main__":
    run_seeds()
