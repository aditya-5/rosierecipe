"""
Recipe by Rosie Scraper - FULLY AUTOMATED
Handles login, print dialog, and creates compact image sheets
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import base64
from PIL import Image
from io import BytesIO
import requests
from PyPDF2 import PdfMerger
import img2pdf
import math
# ========================================
# CONFIGURATION
# ========================================
EMAIL = "aditya.7@outlook.com"  # Replace with your email
PASSWORD = "HELLOaa123,./"  # Replace with your password
OUTPUT_FOLDER = "my_recipes"
PROGRESS_FILE = "recipe_progress.txt"
INCLUDE_IMAGES = True
IMAGES_PER_PAGE = 8  # 2x2 grid per page

# ========================================

def load_progress():
    """Load completed recipes from progress file"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_progress(url):
    """Save completed recipe URL to progress file"""
    with open(PROGRESS_FILE, 'a') as f:
        f.write(url + '\n')

def setup_browser():
    """Setup Chrome browser with kiosk printing enabled"""
    print("Setting up browser...")
    options = Options()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument(f"--user-data-dir=./selenium-profile")
    options.add_argument("--profile-directory=Default")


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    return driver
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login(driver, email, password, skip_manual=False):
    """Automated login to Recipe by Rosie"""
    print("Logging in automatically...")
    
    try:
        driver.get("https://www.recipebyrosie.com")
        time.sleep(3)
        
        # Check if already logged in (no "Log In" button means we're logged in)
        try:
            login_link = driver.find_element(By.LINK_TEXT, "Log In")
        except:
            print("✓ Already logged in (session active)")
            return True
        
        # Step 1: Click main "Log In" button
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log In"))
        )
        login_link.click()
        time.sleep(2)
        
        # Step 2: Click "Already a member? Log In"
        try:
            member_login = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]"))
            )
            member_login.click()
            time.sleep(2)
        except:
            print("  → Already on login form")
        
        # Step 3: Click "Log in with Email"
        try:
            email_login = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in with Email')]"))
            )
            email_login.click()
            time.sleep(2)
        except:
            print("  → Already on email login form")
        
        # Step 4: Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(1)
        
        # Step 5: Enter password
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(1)
        
        # Step 6: Click login button
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for login to complete
        time.sleep(5)
        
        print("✓ Logged in successfully")
        return True
        
    except Exception as e:
        print(f"✗ Automatic login failed: {e}")
        if not skip_manual:
            print("\nPlease log in manually, then press Enter...")
            input()
        return True

def get_recipe_urls(driver):
    """Get all recipe URLs"""
    print("Finding all recipes...")
    driver.get("https://www.recipebyrosie.com/recipes")
    time.sleep(3)
    
    # Scroll to load all
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    # Load more
    try:
        for _ in range(10):
            load_more = driver.find_element(By.XPATH, "//button[contains(text(), 'Load More')]")
            load_more.click()
            time.sleep(2)
    except:
        pass
    
    # Get links
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/post/']")
    urls = []
    for link in links:
        url = link.get_attribute('href')
        if url and '/post/' in url and url not in urls:
            urls.append(url)
    
    print(f"Found {len(urls)} recipes!")
    return urls

def get_recipe_images(driver):
    """Extract recipe images"""
    images = []
    try:
        driver.switch_to.default_content()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        
        for img in img_elements:
            src = img.get_attribute('src')
            if src and 'static.wix' in src and '/media/' in src:
                try:
                    dimensions = driver.execute_script("""
                        var img = arguments[0];
                        return {width: img.naturalWidth, height: img.naturalHeight};
                    """, img)
                    
                    w = dimensions.get('width', 0)
                    h = dimensions.get('height', 0)
                    
                    if w > 250 and h > 250:
                        images.append(src)
                except:
                    pass
        
        # Remove duplicates
        seen = set()
        unique = []
        for img in images:
            if img not in seen:
                seen.add(img)
                unique.append(img)
        
        return unique[:10]
    except Exception as e:
        print(f"  Warning: Could not get images - {e}")
        return []

def download_image(url):
    """Download image"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except:
        return None

def create_compact_image_pdf(images, output_path, images_per_page=4):
    """Create PDF with multiple small images per page using img2pdf"""
    if not images:
        return None
    
    try:
        print(f"  Creating compact image PDF with {images_per_page} images per page...")
        
        # Download all images first
        downloaded = []
        for url in images:
            img = download_image(url)
            if img:
                # Convert to RGB
                if img.mode != 'RGB':
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    else:
                        rgb_img.paste(img)
                    img = rgb_img
                
                # Resize to smaller size (fit in quarter of A4 page)
                max_size = (900, 900)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                downloaded.append(img)
        
        if not downloaded:
            return None
        
        # Create pages with multiple images
        from PIL import ImageDraw
        pages = []
        page_width, page_height = 2550, 3300
        
        for i in range(0, len(downloaded), images_per_page):
            # Create blank page
            page = Image.new('RGB', (page_width, page_height), 'white')
            
            # Get images for this page
            page_images = downloaded[i:i+images_per_page]
            
            # Calculate grid
            cols = 2
            rows = math.ceil(images_per_page / cols)

            cell_width = page_width // cols
            cell_height = page_height // rows
                        
            # Place images in grid
            for idx, img in enumerate(page_images):
                row = idx // cols
                col = idx % cols
                
                # Calculate position (centered in cell)
                x = col * cell_width + (cell_width - img.width) // 2
                y = row * cell_height + (cell_height - img.height) // 2
                
                page.paste(img, (x, y))
            
            pages.append(page)
        
        # Save all pages as PDF
        if pages:
            # Save first page
            for p in pages:
                p.info['dpi'] = (300, 300)
            pages[0].save(
                output_path,
                save_all=True,
                append_images=pages[1:] if len(pages) > 1 else [],
                format='PDF',
                resolution=300.0
            )
            print(f"  ✓ Created PDF with {len(pages)} pages, {len(downloaded)} images total")
            return output_path
        
        return None
        
    except Exception as e:
        print(f"  Warning: Could not create image PDF - {e}")
        import traceback
        traceback.print_exc()
        return None

def merge_pdfs(recipe_pdf, images_pdf, output_pdf):
    """Merge PDFs"""
    try:
        merger = PdfMerger()
        merger.append(recipe_pdf)
        
        if images_pdf and os.path.exists(images_pdf):
            merger.append(images_pdf)
            print(f"  ✓ Merged recipe + images")
        
        merger.write(output_pdf)
        merger.close()
        
        # Clean up
        for f in [recipe_pdf, images_pdf]:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        
        return True
    except Exception as e:
        print(f"  Warning: Merge failed - {e}")
        if os.path.exists(recipe_pdf):
            os.rename(recipe_pdf, output_pdf)
        return False

def click_print_with_image(driver):
    """Click print buttons in iframe"""
    try:
        driver.switch_to.default_content()
        
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        
        print_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ccm-printbutton"))
        )
        print_button.click()
        print("  ✓ Clicked 'Print'")
        time.sleep(1)
        
        with_image = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "ccm-printWithImage"))
        )
        with_image.click()
        print("  ✓ Clicked 'With Image'")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"  ✗ Print click failed: {e}")
        return False
    finally:
        driver.switch_to.default_content()

def save_pdf_from_print_preview(driver, filename, folder):
    """Save PDF directly without print dialog"""
    original = driver.current_window_handle
    time.sleep(2)
    
    all_windows = driver.window_handles
    
    # Switch to print preview if new window opened
    if len(all_windows) > 1:
        for window in all_windows:
            if window != original:
                driver.switch_to.window(window)
                print(f"  ✓ Switched to print preview")
                break
    
    # Save PDF directly (kiosk-printing should prevent dialog)
    temp_pdf = os.path.join(folder, f"{filename}_temp.pdf")
    
    result = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True,
        "landscape": False,
        "paperWidth": 8.5,
        "paperHeight": 11,
        "marginTop": 0.4,
        "marginBottom": 0.4,
        "marginLeft": 0.4,
        "marginRight": 0.4,
    })
    
    with open(temp_pdf, 'wb') as f:
        f.write(base64.b64decode(result['data']))
    
    # Close print window if opened
    if len(all_windows) > 1:
        driver.close()
        driver.switch_to.window(original)
    
    return temp_pdf

def save_recipe(driver, url, number, folder):
    """Save complete recipe with compact images"""
    driver.get(url)
    time.sleep(5)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    # Get title
    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1").text
        clean = "".join(c for c in title if c.isalnum() or c in (' ', '-'))
        filename = f"{number:03d}_{clean.replace(' ', '_')}"
    except:
        filename = f"{number:03d}_recipe"
    
    final_pdf = os.path.join(folder, f"{filename}.pdf")
    
    # Get images
    images = []
    if INCLUDE_IMAGES:
        images = get_recipe_images(driver)
        print(f"  Found {len(images)} images")
    
    # Click print
    if not click_print_with_image(driver):
        raise Exception("Could not click print button")
    
    # Save recipe PDF - let exceptions bubble up
    recipe_pdf = save_pdf_from_print_preview(driver, filename, folder)
    if not recipe_pdf:
        raise Exception("PDF save returned None")
    
    # Create compact image PDF
    images_pdf = None
    if images and INCLUDE_IMAGES:
        images_pdf = os.path.join(folder, f"{filename}_images.pdf")
        images_pdf = create_compact_image_pdf(images, images_pdf, IMAGES_PER_PAGE)
    
    # Merge
    if images_pdf:
        merge_pdfs(recipe_pdf, images_pdf, final_pdf)
    else:
        os.rename(recipe_pdf, final_pdf)
    
    print(f"  ✓ Saved: {filename}.pdf")
    return True

def main():
    print("="*60)
    print("Recipe by Rosie - FULLY AUTOMATED")
    print("="*60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Load progress
    completed = load_progress()
    if completed:
        print(f"Found {len(completed)} already completed recipes")
    
    driver = setup_browser()
    
    try:
        login(driver, EMAIL, PASSWORD)
        urls = get_recipe_urls(driver)
        
        # Filter out completed recipes
        remaining = [url for url in urls if url not in completed]
        
        print(f"\nTotal recipes: {len(urls)}")
        print(f"Already completed: {len(completed)}")
        print(f"Remaining: {len(remaining)}")
        print("="*60)
        
        success = 0
        i = 0
        while i < len(remaining):
            url = remaining[i]
            overall_num = len(urls) - len(remaining) + i + 1
            print(f"\n[{overall_num}/{len(urls)}] {url}")
            try:
                save_recipe(driver, url, overall_num, OUTPUT_FOLDER)
                success += 1
                save_progress(url)
                i += 1  # Only move to next recipe on success
            except Exception as e:
                print(f"⚠️ Error: {str(e)[:100]}")
                print("⚠️ Restarting browser...")
                try:
                    driver.quit()
                except:
                    pass
                driver = setup_browser()
                login(driver, EMAIL, PASSWORD, skip_manual=True)
                print("  Retrying same recipe...")
                # Don't increment i - retry the same recipe

        
        print("\n" + "="*60)
        print("COMPLETE!")
        print("="*60)
        print(f"Saved: {success}/{len(remaining)} recipes")
        print(f"Total completed: {len(completed) + success}/{len(urls)} recipes")
        print(f"Location: {os.path.abspath(OUTPUT_FOLDER)}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    if EMAIL == "your.email@example.com":
        print("\n⚠️  Update EMAIL and PASSWORD first!")
    else:
        main()