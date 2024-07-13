import requests
from typing import List, Dict, Optional, Tuple

app_id = 2923300

def get_inventory_items(steam_id: str, context_id: int = 2) -> Optional[Tuple[List[Dict], List[Dict]]]:
    """
    Получает список предметов из инвентаря Steam по SteamID64.

    :param steam_id: SteamID64 профиля Steam.
    :param context_id: ID контекста инвентаря. По умолчанию 2 для инвентаря игры CS:GO.
    :return: Кортеж с двумя списками: assets и descriptions. Если запрос неудачен, возвращается None.
    """
    url = f'http://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}?l=russian&count=100'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'descriptions' in data:
            return data['assets'], data['descriptions']
        else:
            print(f"Ошибка при получении предметов: {data.get('message', 'Неизвестная ошибка')}")
            return None
    except requests.RequestException as e:
        print(f"Ошибка HTTP запроса: {e}")
        return None

def generate_html(assets: List[Dict], descriptions: List[Dict]):
    """
    Генерирует HTML файл с информацией о предметах инвентаря и их изображениями.

    :param assets: Список активов (предметов) из инвентаря.
    :param descriptions: Список описаний предметов.
    """
    description_dict = {desc['classid']: desc for desc in descriptions}
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Инвентарь Steam</h1>
    '''

    base_url = 'https://community.akamai.steamstatic.com/economy/image/'

    for asset in assets:
        classid = asset['classid']
        if classid in description_dict:
            description = description_dict[classid]
            icon_url = description.get('icon_url', '')
            full_icon_url = base_url + icon_url + '/330x192?allow_animated=1' if icon_url else ''  # Формируем полный URL для картинки
            html_content += f'''
            <div class="item">
                <img src="{full_icon_url}" alt="{description.get('name', '')}">
                <div class="item-info">
                    <h2>{description.get('name', '')}</h2>
                    <p>Type: {description.get('type', 'Неизвестно')}</p>
                    <p>ID: {asset.get('assetid', 'Неизвестен')}</p>
                    <p>Class ID: {description.get('classid', 'Неизвестен')}</p>
                    <p>Marketable: {'Yes' if description.get('marketable', False) else 'No'}</p>
                    <p>Tradable: {'Yes' if description.get('tradable', 0) else 'No'}</p>
                    <p>Commodity: {'Yes' if description.get('commodity', 0) else 'No'}</p>
                    <p>Quantity: {asset.get('amount', 1)}</p>
                    <p>Description: {' '.join(desc.get('value', '') for desc in description.get('descriptions', []))}</p>
                    <p>Market Hash Name: {description.get('market_hash_name', 'Неизвестно')}</p>
                    <div class="tags">
    '''
            if 'tags' in description:
                for tag in description['tags']:
                    html_content += f'<span>{tag.get("localized_tag_name", "")}</span>'

            html_content += '''
                    </div>
                </div>
            </div>
            '''

    html_content += '''
        </div>
    </body>
    </html>
    '''

    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    steam_id = 76561198076702509  # Пример SteamID64 [ Aksel ] :3
    result = get_inventory_items(steam_id)
    if result:
        assets, descriptions = result
        generate_html(assets, descriptions)
        print("HTML файл с информацией о предметах инвентаря успешно создан.")
    else:
        print("Не удалось получить предметы инвентаря.")

if __name__ == '__main__':
    main()
