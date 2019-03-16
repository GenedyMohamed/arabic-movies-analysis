from web_scrapping import simple_get, write_html, read_html, add_to_csv, add_films_to_csv, get_film_details, get_avg_duration, write_avg_durations, get_names, get_synopses




# raw_html = simple_get("https://www.elcinema.com/work/1007952/")
# write_html(raw_html, "page.html")
    
# get_film_details("/work/1002400/")
# get_film_details("/work/1809879/")
# get_film_details("/work/1619698/")
# get_film_details("/work/1006659/")
# dict = {}
# dict.update(get_film_details("/work/1007952/"))
# add_to_csv(dict)            
# get_film_details("/work/1010353/")

# add_films_to_csv()
#write_avg_durations()

# print(get_avg_duration(1949))

print(get_synopses())

