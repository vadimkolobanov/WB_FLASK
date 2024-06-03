from flask import render_template, request, current_app as app
from .models import get_catalogs_wb, get_data_category, scrap_page, get_data_from_json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categories')
def categories():
    catalogs_wb = get_catalogs_wb()
    categories = get_data_category(catalogs_wb)
    return render_template('categories.html', categories=categories)

@app.route('/products/')
def products():
    low_price = request.args.get('low_price', 1, type=int)
    top_price = request.args.get('top_price', 1000000, type=int)
    discount = request.args.get('discount', 0, type=int)
    url = request.args.get('url', type=str)
    url = '/' + url.lstrip('/')
    catalogs_wb = get_catalogs_wb()
    categories = get_data_category(catalogs_wb)

    category = None
    for cat in categories:
        if cat['url'] == url:
            category = cat
            break

    if category:
        data_list = []
        for page in range(1, 2):  # Ограничим для теста до 2 страниц
            data = scrap_page(page, category['shard'], category['query'], low_price, top_price, discount)
            products = get_data_from_json(data)
            if products:
                data_list.extend(products)
            else:
                break
        return render_template('products.html', products=data_list)
    return "Category not found", 404
