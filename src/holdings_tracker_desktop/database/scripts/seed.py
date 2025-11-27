from holdings_tracker_desktop.database.database import SessionLocal
from holdings_tracker_desktop.models.country import Country
from holdings_tracker_desktop.models.currency import Currency
from holdings_tracker_desktop.models.asset_type import AssetType
from holdings_tracker_desktop.models.broker import Broker

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
            AssetType(name="Ação"),
            AssetType(name="Fiagro"),
            AssetType(name="FI-Infra"),
            AssetType(name="FII"),
            AssetType(name="Reit"),
            AssetType(name="Stock")
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
