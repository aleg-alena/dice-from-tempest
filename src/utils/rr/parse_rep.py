from bs4 import BeautifulSoup

DONATION_NAME = 'Пожертвование'
TODAY_NAME = 'Сегодня'
YESTODAY_NAME = 'Вчера'


def parse_html_replenishments(page: str) -> list[dict[str, int]]:
    replenishments = []
    soup = BeautifulSoup(page, 'html.parser')

    elements = soup.find_all('tr', class_='list_link')

    for element in elements:
        donation = element.find('td', class_='list_log_m')

        try:
            donation_text_money = element.find('td', class_='money_log').text
        except AttributeError:
            continue

        if not DONATION_NAME in donation.text or not '+' in donation_text_money:
            continue

        donation_amount = int(donation_text_money.split('R')[0][2:][:-1].replace('.', ''))

        profile_id = int(donation.find('span', class_='results_date dot hov2')['action']\
                        .replace('slide/profile/', ''))
        time = int(element.find('div', class_='log_dates')
                   .text.replace(TODAY_NAME, '').replace(YESTODAY_NAME, '')
                   .replace(' ', '').replace(':', ''))

        replenishments.append(dict(profile_id=profile_id, amount=donation_amount, time=time))

    return replenishments
