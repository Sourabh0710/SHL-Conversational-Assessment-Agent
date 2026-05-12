from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time

# LOAD EXISTING CATALOG
with open(
    "data/processed/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    assessments = json.load(f)

options = webdriver.ChromeOptions()

# Uncomment for silent mode
# options.add_argument("--headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)

enriched_assessments = []

for i, assessment in enumerate(assessments):

    print(f"\n[{i+1}/{len(assessments)}]")
    print(f"SCRAPING: {assessment['name']}")

    url = assessment["url"]

    try:

        driver.get(url)

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        time.sleep(3)

        page_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        # BASIC ENRICHMENT
        enriched = {
            "name": assessment["name"],
            "url": assessment["url"],
            "attributes": assessment["attributes"],
            "page_text": page_text[:5000]
        }

        enriched_assessments.append(enriched)

        print("SUCCESS")

    except Exception as e:

        print("FAILED")

        continue

driver.quit()

# SAVE ENRICHED DATASET
with open(
    "data/processed/shl_catalog_enriched.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(enriched_assessments, f, indent=2)

print("\nENRICHED DATASET SAVED")