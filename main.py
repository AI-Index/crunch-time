import time
import csv

from lib import db, api


def print_dict(d):
    print("\n".join(["%s: %s" % (k, v) for (k, v) in sorted(d.items())]))


def download_funding_info(conn, curr):
    companies = db.select_companies(conn, curr)

    company_funding_info = db.select_companies_with_funding(conn, curr)
    print("Filtering out existing companies ...")
    companies = [c for c in companies if c["company_uuid"] not in company_funding_info]
    print("Done.")
    print(len(companies))
    for company in companies:
        permalink = company["company_permalink"]
        company_uuid = company["company_uuid"]
        try:
            print("Fetching data for: ", permalink)
            funding_rounds = api.fetch_company_funding_details(permalink)
            for round_ in funding_rounds:
                db.insert_funding(conn, curr, company_uuid, round_)
        except Exception as e:
            print("ERROR WITH COMPANY %s" % company_uuid)
            print(e)
            print("------")
            time.sleep(10)


def print_locations():
    locations = api.fetch_locations()
    cities = list(sorted(list(locations["city"])))
    countries = list(sorted(list(locations["country"])))
    continents = list(sorted(list(locations["continent"])))

    print("Cities")
    print("\n".join(cities))
    print("---")
    print("Countries")
    print("\n".join(countries))
    print("---")
    print("Continents")
    print("\n".join(continents))
    print("---")


if __name__ == "__main__":
    conn, curr, err = db.open_connection(dbname='crunchy')
    if err: 
        quit()

    # Populate the CATEGORIES table
    db.injest_categories(conn, curr)
    # Request data on all companies which fall into the AI
    # categories defined in db.py
    db.injest_ai_companies(conn, curr)

    # Use that list of companies to get funding info
    print("Downloading funding data. This will take 1+ hours.")
    download_funding_info(conn, curr)
    print("Done.")

    # Use that data to calculate funding by year
    csv_file = 'funding_per_year_by_country.csv'
    with open(csv_file, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(db.countries)
        for year in range(1992, 2019):
            year_row = []
            for country in db.countries:
                year_total = db.select_funding_by_year(conn, curr, year, country=country)
                year_row.append(year_total)
            writer.writerow(year_row)
