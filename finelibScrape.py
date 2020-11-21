import csv
import requests
from bs4 import BeautifulSoup

csv_file = open('FineLibScraped.csv','w', encoding='utf-8')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Business Name', 'Business Number', 'Business Address', 'Business Short Description', 'Website', 'Location','Email Contact', 'Verified'])

web_main_src = requests.get('https://finelib.com').text
web_main_soup = BeautifulSoup(web_main_src, 'lxml')
state_categories = web_main_soup.find('div', class_='box-682 bg-none')
scraped_states = {}

for state in state_categories.find_all('li'):
    for state_links in state.find_all('a'):
        state_name = state_links.text
        state_href = state_links['href']
        scraped_states[state_name] = state_href

for state_name in scraped_states.keys():
    state_src = requests.get(f'https://finelib.com{scraped_states[state_name]}').text
    state_soup = BeautifulSoup(state_src, 'lxml')
    state_categories = state_soup.find('div', class_='city-list-inner city-list-col')
    category_links = []
    location = state_name

    for category in state_categories.find_all('li'):
        for category_link in category.find_all('a'):
            category_href = category_link['href']
            category_links.append(category_href)

    for link in category_links:
        link_category_src = requests.get(f'https://www.finelib.com{link}').text
        link_category_soup = BeautifulSoup(link_category_src, 'lxml')

        for business_soup in link_category_soup.find_all('div', class_='box-682 bg-none'):
            business_name = business_soup.find('div', class_='box-headings box-new-hed').a.text
            business_more_info = business_soup.find('div', class_='cmpny-lstng url').a['href']
            main_info_page_url = requests.get(business_more_info).text
            main_page_soup = BeautifulSoup(main_info_page_url, 'lxml').find('div', class_='box-682 bg-none')

            business_address = main_page_soup.find('div', class_='cmpny-lstng-1').text
            business_hotline = main_page_soup.find('div', class_='tel-no-div').div.text
            business_hotline = business_hotline.split(',')
            try:
                business_website = main_page_soup.find('div', class_='cmpny-lstng url').a['href']
            except Exception as e:
                business_website = None

            sub_Bx = {}
            for mail_info in main_page_soup.find_all('div', class_='subb-bx MT-15'):
                try:
                    sub_Bx[mail_info.h3.text] = mail_info.p.text
                except Exception as e:
                    sub_Bx.update({'mail\\info':None})
            for info in sub_Bx.keys():
                try:
                    business_email = sub_Bx['E-mail Contact']
                except Exception as e:
                    business_email = None
                try:
                    business_short_info = sub_Bx['Short Description']
                except Exception as e:
                    business_short_info = None
            try:
                if main_page_soup.find('div', class_='box-headings box-new-hed').img[
                    'src'] == '//www.finelib.com/images/verified.png':
                    verified = True
            except Exception as e:
                verified = False
            csv_writer.writerow([business_name, business_hotline, business_address, business_short_info, business_website, location, business_email, verified])

        try:
            category_list = link_category_soup.find('div', class_='category-list newlist')
            for category_link in category_list.find_all('li'):
                for link in category_link.find_all('a'):
                    page_link = link['href']
                    link_src = requests.get(f'https://www.finelib.com/cities/lagos{link}{page_link}').text
                    link_soup = BeautifulSoup(link_src, 'lxml')

                    for business_soup in link_soup.find_all('div', class_='box-682 bg-none'):
                        business_name = business_soup.find('div', class_='box-headings box-new-hed').a.text
                        business_more_info = business_soup.find('div', class_='cmpny-lstng url').a['href']
                        main_info_page_url = requests.get(business_more_info).text
                        main_page_soup = BeautifulSoup(main_info_page_url, 'lxml').find('div', class_='box-682 bg-none')

                        business_address = main_page_soup.find('div', class_='cmpny-lstng-1').text
                        business_hotline = main_page_soup.find('div', class_='tel-no-div').div.text
                        business_hotline = business_hotline.split(',')
                        try:
                            business_website = main_page_soup.find('div', class_='cmpny-lstng url').a['href']
                        except Exception as e:
                            business_website = None

                        sub_Bx = {}
                        for mail_info in main_page_soup.find_all('div', class_='subb-bx MT-15'):
                            try:
                                sub_Bx[mail_info.h3.text] = mail_info.p.text
                            except Exception as e:
                                sub_Bx.update({'mail\\info':None})
                        for info in sub_Bx.keys():
                            try:
                                business_email = sub_Bx['E-mail Contact']
                            except Exception as e:
                                business_email = None
                            try:
                                business_short_info = sub_Bx['Short Description']
                            except Exception as e:
                                business_info = None
                        try:
                            if main_page_soup.find('div', class_='box-headings box-new-hed').img[
                                'src'] == '//www.finelib.com/images/verified.png':
                                verified = True
                        except Exception as e:
                            verified = False
                        csv_writer.writerow(
                            [business_name, business_hotline, business_address, business_short_info, business_website, location, business_email, verified])

                    try:
                        next_category_list = link_soup.find('div', class_='category-list newlist')
                        for next_category_link in next_category_list.find_all('li'):
                            for next_link in next_category_link.find_all('a'):
                                next_page_link = next_link['href']
                                next_page_src = requests.get(f'https://www.finelib.com{next_page_link}').text
                                next_page_soup = BeautifulSoup(next_page_src, 'lxml')

                                for business_soup in next_page_soup.find('div', class_='box-682 bg-none'):
                                    business_name = business_soup.find('div', class_='box-headings box-new-hed').a.text
                                    business_more_info = business_soup.find('div', class_='cmpny-lstng url').a['href']
                                    main_info_page_url = requests.get(business_more_info).text
                                    main_page_soup = BeautifulSoup(main_info_page_url, 'lxml').find('div',
                                                                                                    class_='box-682 bg-none')

                                    business_address = main_page_soup.find('div', class_='cmpny-lstng-1').text
                                    business_hotline = main_page_soup.find('div', class_='tel-no-div').div.text
                                    business_hotline = business_hotline.split(',')
                                    try:
                                        business_website = main_page_soup.find('div', class_='cmpny-lstng url').a['href']
                                    except Exception as e:
                                        business_website = None

                                    sub_Bx = {}
                                    for mail_info in main_page_soup.find_all('div', class_='subb-bx MT-15'):
                                        try:
                                            sub_Bx[mail_info.h3.text] = mail_info.p.text
                                        except Exception as e:
                                            sub_Bx.update({'mail\\info':None})
                                    for info in sub_Bx.keys():
                                        try:
                                            business_email = sub_Bx['E-mail Contact']
                                        except Exception as e:
                                            business_email = None
                                        try:
                                            business_short_info = sub_Bx['Short Description']
                                        except Exception as e:
                                            business_info = None
                                    try:
                                        if main_page_soup.find('div', class_='box-headings box-new-hed').img[
                                            'src'] == '//www.finelib.com/images/verified.png':
                                            verified = True
                                    except Exception as e:
                                        verified = False
                                    csv_writer.writerow(
                                        [business_name, business_hotline, business_address, business_short_info, business_website, location, business_email, verified])
                    except Exception as e:
                        next_category_list = None
        except Exception as e:
            category_list = None

csv_file.close()
