from django.shortcuts import render
from django.http import HttpResponse
import asyncio
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from asgiref.sync import async_to_sync
import os

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

def setup_driver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Example: Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppresses DevTools logs.
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    chrome_options.add_argument('--disable-stylesheets')  # Experiment with disabling stylesheets

    # Set up Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_population_with_selenium():
    driver = setup_driver()
    try:
        driver.get("https://www.worldometers.info/world-population/")
        # Wait for the element to be loaded
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".maincounter-number span"))
        )
        population = element.text
        return population
    finally:
        driver.quit()


def scrape_worldometer_data():
    driver = setup_driver()
    url = "https://www.worldometers.info/world-population/"
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-sm-6"))
        )
        data = {
            'births_today': driver.find_element(By.CSS_SELECTOR, "[rel='births_today']").text,
            'deaths_today': driver.find_element(By.CSS_SELECTOR, "[rel='dth1s_today']").text,
            'population_growth_today': driver.find_element(By.CSS_SELECTOR, "[rel='absolute_growth']").text,
            'births_this_year': driver.find_element(By.CSS_SELECTOR, "[rel='births_this_year']").text.replace(',', ''),
            'deaths_this_year': driver.find_element(By.CSS_SELECTOR, "[rel='dth1s_this_year']").text.replace(',', ''),
            'expenditure_this_year': driver.find_element(By.CSS_SELECTOR,"[rel='gov_expenditures_health/today']").text.replace(',', ''),
            
            # Add further selectors for yearly data if available on the same page
        }
    finally:
        driver.quit()
    
    return data




def scrape_expenditure_data():
    driver = setup_driver()
    url = "https://www.worldometers.info/"
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gov_expenditures_health"))
        )
        data = {
            "World_population":driver.find_element(By.CSS_SELECTOR, "[rel='current_population']").text,
            "Births_this_year":driver.find_element(By.CSS_SELECTOR, "[rel='births_this_year']").text,
            "Births_today":driver.find_element(By.CSS_SELECTOR, "[rel='births_today']").text,
            "Deaths_this_year":driver.find_element(By.CSS_SELECTOR, "[rel='dth1s_this_year']").text,
            "Death_today":driver.find_element(By.CSS_SELECTOR, "[rel='dth1s_today']").text,
            'Healthcare_expenditure_this_year':"$"+ driver.find_element(By.CSS_SELECTOR, "[rel='gov_expenditures_health/today']").text,
            'Education_expenditure_this_year': "$"+driver.find_element(By.CSS_SELECTOR, "[rel='gov_expenditures_education/today']").text,
            'Cars_produced_this_year': driver.find_element(By.CSS_SELECTOR, "[rel='automobile_produced/this_year']").text,
            'Computers_produced_this_year': driver.find_element(By.CSS_SELECTOR, "[rel='computers_sold/this_year']").text,
             "New_book_titles_published":driver.find_element(By.CSS_SELECTOR, "[rel='books_published/this_year']").text,
             "Newspaper_circilated_today":driver.find_element(By.CSS_SELECTOR, "[rel='newspapers_circulated/today']").text,
             "Money_spent_on_vediogames":"$"+driver.find_element(By.CSS_SELECTOR, "[rel='videogames/today']").text,
             "Internet_users_today":driver.find_element(By.CSS_SELECTOR, "[rel='internet_users']").text,
             "Email_sent_today":driver.find_element(By.CSS_SELECTOR, "[rel='em/today']").text,
             "Google_searches_today":driver.find_element(By.CSS_SELECTOR, "[rel='google_searches/today']").text,
             "Forest_lost_this_year":driver.find_element(By.CSS_SELECTOR, "[rel='forest_loss/this_year']").text,
             "Co2_emmision_this_year":driver.find_element(By.CSS_SELECTOR, "[rel='co2_emissions/this_year']").text,
             "Overweight_people":driver.find_element(By.CSS_SELECTOR, "[rel='overweight']").text,
             "Obese_people":driver.find_element(By.CSS_SELECTOR, "[rel='obese']").text,
             "Died_of_hunger":driver.find_element(By.CSS_SELECTOR, "[rel='dth1_hunger/today']").text,
             "Water_consumed":driver.find_element(By.CSS_SELECTOR, "[rel='water_consumed/this_year']").text,
             "Energy_consumed":driver.find_element(By.CSS_SELECTOR, "[rel='energy_used/today']").text,
             "Oil_consumption":driver.find_element(By.CSS_SELECTOR, "[rel='oil_consumption']").text,
             "Natural_gas_left":driver.find_element(By.CSS_SELECTOR, "[rel='gas_reserves']").text,
             "Abortion":driver.find_element(By.CSS_SELECTOR, "[rel='ab/this_year']").text,
             "HIV_AIDS_infected_people":driver.find_element(By.CSS_SELECTOR, "[rel='infections_hiv']").text,
             "Cigerates_smoked":driver.find_element(By.CSS_SELECTOR, "[rel='cigarettes_smoked/today']").text,
             "Death_caused_by_smoking":driver.find_element(By.CSS_SELECTOR, "[rel='dth1s_cigarettes/this_year']").text,
             "Death_caused_by_alchol":driver.find_element(By.CSS_SELECTOR, "[rel='dth1s_alchool/this_year']").text,
             "Sucide":driver.find_element(By.CSS_SELECTOR, "[rel='sui/this_year']").text,
            # Add further selectors for yearly data if available on the same page
        }
    finally:
        driver.quit()
    
    return data


def members(request):
    return HttpResponse("Hello world!")

def population_view(request):
    try:
        population = fetch_population_with_selenium()
        return HttpResponse(population)
    except Exception as e:
        return HttpResponse(f"Failed to retrieve data: {str(e)}", status=500)


#birth and death views

async def birth_and_death_view(request):
    # Your asynchronous view content here
    return JsonResponse({"message": "This is an async view"})



def worldometer_view(request):
    try:
        data = scrape_worldometer_data()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def worldometer_expenditure_view(request):
    try:
        data = scrape_expenditure_data()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    



