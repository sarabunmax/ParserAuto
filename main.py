import UserConfig as UC
import DataProcessor as DP


config = UC.Config()  # object container with configuration parametrs
URL = f'https://www.olx.ua/d/uk/transport/legkovye-avtomobili/{config.mark}/?currency=USD&search%5Bfilter_enum_model' \
      f'%5D%5B0%5D={config.model}'  # URL link for parsing

try:
    html_page = DP.get_html(URL)  # html code recived from web page
    print('Почалась обробка данних. Будь ласка зачекайте завершення...')
    vechicle_data = []  # storage for saving clean data

    # block variables for checking last page
    page_numb = 1
    autos_info = []
    last_size = 1

    # cycle for processing each web page
    while True:

        if len(autos_info) != last_size:
            last_size = len(autos_info)
            DP.html_parsing(html_page, vechicle_data)
            page_numb += 2
        else:
            break

    DP.write_data(vechicle_data, config)  # writing clean data ti csv file
    DP.gistograme(vechicle_data, config)  # building plot for price analyze
    print('Обробка данних завершена успішно. Файли згенеровані.')

except ConnectionError:
    print('Помилка з\'єднання з сервером. Перевірте правильність данних конфігурації та спробуйте ще раз.')
    exit()


