from webCrawlerStarterkit import *
driver.get('https://www.pdfdrive.com')
book_list = {}

try:
    def search_for_book(bookName):
        search = driver.find_element_by_id('form-container').find_element_by_name('q')
        search.clear()
        search.send_keys(bookName)
        search.send_keys(Keys.RETURN)


    def book_items(limit=5):
        search_for_book("Dart")
        page = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dialog-main'))
        )
        books = page.find_element_by_class_name('files-new')
        book_links = books.find_elements_by_tag_name('a')
        book_img = books.find_elements_by_tag_name('img')
        for book in book_links:
            for img in book_img:
                book_list[book.text] = [book.get_attribute('href'), img.get_attribute('src')]
        return book_list


    def display_search_result():
        book_items()
        for extracted_book in book_list.items():
            print(extracted_book)


    def get_download_link(selected_book):
        driver.get(book_list.get(selected_book)[0])
        image_url = book_list.get(selected_book)[1]
        download_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'download-button-link')))
        download_button.click()
        download_link = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Download ( PDF )'))
        )
        print(download_link.get_attribute('href'))
        print(image_url)

finally:
    driver.quit()
