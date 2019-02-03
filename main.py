from web_scrapping import simple_get, write_html, read_html, add_to_csv

raw_html = simple_get('https://www.elcinema.com/index/work/release_year/1979?page=10')
write_html(raw_html)

# loop on all html
for line in read_html(raw_html):
    # get info per movie and add to csv
    add_to_csv('1940', 'test_title', 'test_description', '6.2', '["mervat amin", "farid el atrash"]')
    