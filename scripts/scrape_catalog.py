from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import json
import time

BASE_URL = (
    "https://www.shl.com/solutions/products/"
    "product-catalog/?start={}&type=1"
)

options = webdriver.ChromeOptions()

# Uncomment this if you want headless mode
# options.add_argument("--headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)

all_assessments = []
visited_names = set()

# 12 assessments per page
for start in range(0, 240, 12):

    url = BASE_URL.format(start)

    print(f"\nSCRAPING: {url}")

    driver.get(url)

    try:
        # WAIT FOR TABLE TO LOAD
        wait.until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "custom__table-wrapper"
                )
            )
        )

    except:
        print("Table failed to load.")
        continue

    time.sleep(3)

    rows = driver.find_elements(By.TAG_NAME, "tr")

    print(f"ROWS FOUND: {len(rows)}")

    # ONLY START SCRAPING AFTER
    # "Individual Test Solutions"
    inside_individual_section = False

    for row in rows:

        text = row.text.strip()

        if not text:
            continue

        # START SCRAPING HERE
        if "Individual Test Solutions" in text:
            inside_individual_section = True
            continue

        # SKIP EVERYTHING BEFORE INDIVIDUAL SECTION
        if not inside_individual_section:
            continue

        lines = text.split("\n")

        # SKIP TABLE HEADER ROWS
        if (
            "Remote Testing" in text
            or "Adaptive/IRT" in text
            or "Test Type" in text
        ):
            continue

        if len(lines) < 2:
            continue

        # EXTRACT NAME + URL
        try:

            link_element = row.find_element(By.TAG_NAME, "a")

            name = link_element.text.strip()

            assessment_url = link_element.get_attribute("href")

        except:
            continue

        # AVOID DUPLICATES
        if name in visited_names:
            continue

        visited_names.add(name)

        assessment = {
            "name": name,
            "url": assessment_url,
            "attributes": lines[1:]
        }

        all_assessments.append(assessment)

driver.quit()

print(f"\nTOTAL INDIVIDUAL ASSESSMENTS: {len(all_assessments)}\n")

# PRINT SAMPLE
for assessment in all_assessments[:15]:
    print(json.dumps(assessment, indent=2))

# SAVE JSON
with open(
    "data/processed/shl_catalog.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(all_assessments, f, indent=2)

print("\nJSON SAVED SUCCESSFULLY")