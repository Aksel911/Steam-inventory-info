import time

import requests
from typing import List, Dict, Optional, Tuple


app_id_to_name = {
    2923300: 'Banana',
    2977660: 'Cats',
    3046430: 'Hamster',
    3056600: 'Apple Clicker',
    3058700: 'Banana Cat',
    3057390: 'Banana Monkeys',
    3056550: 'Bananamana',
    3013470: 'Bananametr',
    2968430: 'Beer Simulator',
    2947380: 'Clickout',
    3059750: 'Cock',
    3065860: 'Coconut',
    529240: 'Creature Clicker: Capture Train Ascend',
    3015610: 'Banana & Cucumber',
    3069620: 'Dog',
    3059300: 'DOG',
    3057940: 'Ducks',
    3062750: 'DUCKS',
    2784840: 'Egg',
    3017120: 'Egg Surprise',
    3056880: 'Emoji Clicker Collector',
    2996990: 'Flag Clicker',
    1587070: 'Fruits',
    3055390: 'Giraffe',
    2794860: 'Grow a Carrot',
    3022740: 'Heart Clicker',
    2813960: 'Lass ich Sliden',
    3066830: 'Lemon',
    3065090: 'Meh',
    3050630: 'Melon',
    3061500: 'Mob Trader',
    3062410: 'Pizzeria',
    1506810: 'Poop',
    3048820: 'Raspberry',
    3054490: 'Shrimp',
    3047030: 'Tapple: Idle Clicker',
    3059220: 'Watermelon',
    2376170: 'Hamster Combat',
    3056370: 'Honey Peach Clicker',
    3071740: 'Box Clicker',
    3057850: 'Milk',
    3064950: 'Crazy Corn',
    2373450: 'Watermelon'
}

# Определение категорий редкости и их цвета
CatsRarity = {
    'Immortal': '#ffca28',
    'Legendary': '#fa6775',
    'Mythical': '#981f84',
    'Rare': '#41bdeb',
    'Uncommon': '#b0b0b0',
    'COLORED Common': '#d9d9d9',
    'COLORED Legendary': '#fa6775',
    'COLORED Immortal': '#ffca28',
    'COLORED Mythical': '#981f84',
    'COLORED Rare': '#41bdeb',
    'COLORED Uncommon': '#697176',
    'Incredible': '#c21e1d',
    'Colored': '#b38669',
    'Rainbow': '#d57af6',
    'Money': '#1caa6e',
    'Black': '#d3d3d3',
    'Case': '#fc8b38'
}

Rarity = {
    'Promo': '#E1B07E',
    'Ultra rare': '#D19C97',
    'Timeless': '#000080',
    'Exceptional': '#D65076',
    'Mythic': '#e83f5b',
    'Epic': '#6e3f3f',
    'Skin': '#4a90e2'
}


def get_inventory_items(steam_id: str, app_ids: List[int], context_id: int = 2) -> Optional[
    Dict[int, Tuple[List[Dict], List[Dict]]]]:
    """
    Получает список предметов из инвентаря Steam по SteamID64 для нескольких app_id.

    :param steam_id: SteamID64 профиля Steam.
    :param app_ids: Список ID приложений (игр), для которых нужно получить инвентарь.
    :param context_id: ID контекста инвентаря. По умолчанию 2 для инвентаря игры CS:GO.
    :return: Словарь, где ключи - app_id, а значения - кортежи с двумя списками: assets и descriptions. Если запрос неудачен, возвращается None.
    """
    inventories = {}
    for app_id in app_ids:
        app_name = app_id_to_name.get(app_id, 'Unknown Game')
        time.sleep(10)
        url = f'http://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}?l=russian&count=1000'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'descriptions' in data:
                inventories[app_id] = (data['assets'], data['descriptions'])
            else:
                print(f"Ошибка при получении предметов для {app_name} | app_id {app_id}: {data.get('message', 'Неизвестная ошибка')}")
        except requests.RequestException as e:
            print(f"Ошибка HTTP запроса для {app_name} | app_id {app_id}: {e}")
    if inventories:
        return inventories
    else:
        return None


def generate_html(inventories: Dict[int, Tuple[List[Dict], List[Dict]]]):
    """
    Генерирует HTML файл с информацией о предметах инвентаря и их изображениями для нескольких игр.

    :param inventories: Словарь с данными инвентаря по app_id.
    """
    base_url = 'https://community.akamai.steamstatic.com/economy/image/'

    html_content = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Инвентарь Steam</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .tabs {
                display: flex;
                cursor: pointer;
                margin-bottom: 10px;
            }
            .tab-button {
                padding: 10px 15px;
                background: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px 5px 0 0;
                margin-right: 5px;
            }
            .tab-button.active {
                background: #0056b3;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }
            .item {
                display: flex;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid #ddd;
            }
            .item img {
                width: 220px;
                margin-right: 15px;
            }
            .item-info {
                flex: 1;
            }
            .item-info h2 {
                margin: 0 0 5px;
                font-size: 16px;
            }
            .item-info p {
                margin: 0;
                font-size: 14px;
            }
            .item-info .tags {
                margin-top: 10px;
            }
            .item-info .tags span {
                display: inline-block;
                background: #eee;
                padding: 3px 6px;
                border-radius: 4px;
                margin-right: 5px;
                font-size: 12px;
            }

            .item-info .tags span.Common { background: #f2f2f2; }
            .item-info .tags span.Immortal { background: #ffca28; color: #fff; }
            .item-info .tags span.Legendary { background: #fa6775; color: #fff; }
            .item-info .tags span.Mythical { background: #981f84; color: #fff; }
            .item-info .tags span.Rare { background: #41bdeb; color: #fff; }
            .item-info .tags span.Uncommon { background: #b0b0b0; }
            .item-info .tags span.COLORED Common { background: #d9d9d9; }
            .item-info .tags span.COLORED Legendary { background: #fa6775; color: #fff; }
            .item-info .tags span.COLORED Immortal { background: #ffca28; color: #fff; }
            .item-info .tags span.COLORED Mythical { background: #981f84; color: #fff; }
            .item-info .tags span.COLORED Rare { background: #41bdeb; color: #fff; }
            .item-info .tags span.COLORED Uncommon { background: #697176; color: #fff; }
            .item-info .tags span.Incredible { background: #c21e1d; color: #fff; }
            .item-info .tags span.Colored { background: #b38669; color: #fff; }
            .item-info .tags span.Rainbow { background: #d57af6; color: #fff; }
            .item-info .tags span.Money { background: #1caa6e; color: #fff; }
            .item-info .tags span.Black { background: #d3d3d3; color: #fff; }
            .item-info .tags span.Case { background: #fc8b38; color: #fff; }

            .item-info .tags span.Exceptional { background: #D65076; color: #fff; }
            .item-info .tags span.Timeless { background: #000080; color: #fff; }
            .item-info .tags span.Ultra rare { background: #D19C97; color: #fff; }
            .item-info .tags span.Promo { background: #E1B07E; color: #fff; }
            .item-info .tags span.Legendary { background: #ffcc00; color: #333; }
            .item-info .tags span.Mythic { background: #e83f5b; color: #fff; }
            .item-info .tags span.Epic { background: #6e3f3f; color: #fff; }
            .item-info .tags span.Skin { background: #4a90e2; color: #fff; }

            .sort-buttons {
                margin-bottom: 20px;
            }
            .sort-buttons button {
                padding: 10px 15px;
                margin-right: 5px;
                background: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .sort-buttons button:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Инвентарь Steam</h1>
            <div class="sort-buttons">
                <button onclick="sortItems('name')">Сортировать по имени</button>
                <button onclick="sortItems('rarity')">Сортировать по редкости</button>
            </div>
            <div class="tabs">
    '''

    for app_id in inventories.keys():
        app_name = app_id_to_name.get(app_id, 'Unknown Game')

        game_name = f"Игра {app_id}"  # Замените это на название игры, если оно известно
        html_content += f'<button class="tab-button" onclick="openTab(event, \'game-{app_id}\')">{app_name}</button>'

    html_content += '''
            </div>
            <div class="tab-content-container">
    '''

    for app_id, (assets, descriptions) in inventories.items():
        html_content += f'<div id="game-{app_id}" class="tab-content">'

        description_dict = {desc['classid']: desc for desc in descriptions}

        for asset in assets:
            classid = asset['classid']
            if classid in description_dict:
                description = description_dict[classid]
                icon_url = description.get('icon_url', '')
                full_icon_url = base_url + icon_url + '/330x192?allow_animated=1' if icon_url else ''  # Формируем полный URL для картинки

                rarity = 'Common'
                for tag in description.get('tags', []):
                    if tag.get('localized_tag_name', '') in CatsRarity or Rarity:
                        rarity = tag['localized_tag_name']

                html_content += f'''
                <div class="item" data-name="{description.get('name', '')}" data-rarity="{rarity}">
                    <img src="{full_icon_url}" alt="{description.get('name', '')}">
                    <div class="item-info">
                        <h2 style="color: #{description.get('name_color', '')}">{description.get('name', '')}</h2>
                        <div class="tags">
                            <p>Rarity: <span class="{rarity}">{rarity}</span></p>
                        </div>

                        <p>ID: {asset.get('assetid', 'Неизвестен')}</p>
                        <p>Class ID: {description.get('classid', 'Неизвестен')}</p>
                        <p>Marketable: {'Yes' if description.get('marketable', False) else 'No'}</p>
                        <p>Tradable: {'Yes' if description.get('tradable', 0) else 'No'}</p>
                        <p>Commodity: {'Yes' if description.get('commodity', 0) else 'No'}</p>
                        <p>Description: {' '.join(desc.get('value', '') for desc in description.get('descriptions', []))}</p>
                    </div>
                </div>
                '''
        html_content += '</div>'

    html_content += '''
        </div>
        <script>
            function openTab(evt, tabId) {
                const tabs = document.querySelectorAll('.tab-content');
                const buttons = document.querySelectorAll('.tab-button');
                tabs.forEach(tab => tab.classList.remove('active'));
                buttons.forEach(button => button.classList.remove('active'));
                document.getElementById(tabId).classList.add('active');
                evt.currentTarget.classList.add('active');
            }

            function sortItems(criteria) {
                const tabContents = document.querySelectorAll('.tab-content.active');
                tabContents.forEach(tabContent => {
                    const itemList = tabContent;
                    const items = Array.from(itemList.getElementsByClassName('item'));
                    items.sort((a, b) => {
                        if (criteria === 'name') {
                            return a.dataset.name.localeCompare(b.dataset.name);
                        } else if (criteria === 'rarity') {
                            const rarityOrder = ['Common', 'Uncommon', 'Rare', 'Mythical', 'Legendary', 'Immortal', 'Incredible', 'Rainbow', 'Money', 'Black', 'Case'];
                            return rarityOrder.indexOf(a.dataset.rarity) - rarityOrder.indexOf(b.dataset.rarity);
                        }
                        return 0;
                    });
                    itemList.innerHTML = '';
                    items.forEach(item => itemList.appendChild(item));
                });
            }

            document.addEventListener('DOMContentLoaded', () => {
                document.querySelector('.tab-button').click();
            });
        </script>
    </body>
    </html>
    '''

    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    steam_id = '76561198076702509'  # Пример SteamID64

    list_iid = []
    for i in app_id_to_name.items():
        iid = i[0]
        iname = i[1]
        print(iid, iname)
        list_iid.append(iid)

    #list_iid = [iid]
    print(list_iid)
    app_ids = list_iid  # Пример app_id для разных игр
    inventories = get_inventory_items(steam_id, app_ids)
    if inventories:
        generate_html(inventories)
        print("HTML файл с информацией о предметах инвентаря успешно создан.")
    else:
        print("Не удалось получить предметы инвентаря.")


if __name__ == '__main__':
    main()
