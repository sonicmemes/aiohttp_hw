from aiohttp import web
import json
from datetime import datetime

# Временное хранилище для объявлений
ads = []

async def get_ad(request):
    ad_id = request.match_info.get('ad_id')
    if ad_id:
        ad_id = int(ad_id)
        ad = next((ad for ad in ads if ad['id'] == ad_id), None)
        if ad:
            return web.json_response(ad)
        return web.json_response({'message': 'Ad not found'}, status=404)
    return web.json_response(ads)

async def post_ad(request):
    new_ad = await request.json()

    # Проверка на наличие всех необходимых полей
    required_fields = ['title', 'description', 'owner']
    for field in required_fields:
        if field not in new_ad:
            return web.json_response({'error': f'Missing field: {field}'}, status=400)

    new_ad['id'] = len(ads) + 1
    new_ad['created_at'] = datetime.now().isoformat()
    ads.append(new_ad)
    return web.json_response(new_ad, status=201)

async def delete_ad(request):
    ad_id = int(request.match_info['ad_id'])
    global ads
    ads = [ad for ad in ads if ad['id'] != ad_id]
    return web.json_response({'message': 'Ad deleted'})

async def put_ad(request):
    ad_id = int(request.match_info['ad_id'])
    ad = next((ad for ad in ads if ad['id'] == ad_id), None)
    if not ad:
        return web.json_response({'message': 'Ad not found'}, status=404)
    updated_data = await request.json()
    ad.update(updated_data)
    return web.json_response(ad)

app = web.Application()
app.router.add_get('/ads', get_ad)
app.router.add_get('/ads/{ad_id}', get_ad)
app.router.add_post('/ads', post_ad)
app.router.add_delete('/ads/{ad_id}', delete_ad)
app.router.add_put('/ads/{ad_id}', put_ad)

if __name__ == '__main__':
    web.run_app(app, port=8080)
