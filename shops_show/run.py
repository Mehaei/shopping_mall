import flask
from flask import render_template
from models import Shop,db,app

# 启动调试模式
app.debug = True

# 绑定路由和视图函数

# 主页
@app.route('/')
def index():
    # 查询数据
    shop_ml = Shop.query.filter(Shop.source == 'ml').count()
    shop_jd = Shop.query.filter(Shop.source == 'jd').count()
    shop_tb = Shop.query.filter(Shop.source == 'tb').count()
    shop_list = {'jd':["京东商城",shop_jd],'ml':['美丽说',shop_ml],'tb':["淘宝商城",shop_tb]}
    # shop_list = [shop_jd,shop_tb,shop_ml]
    return render_template('index.html',shop_list = shop_list)



# 列表页

@app.route('/shop_list/<classify>')
def shop_list(classify):
    # 查询全部数据
    if classify == 'all':
        shops = Shop.query.order_by('crawl_time').limit(30)
    #     查询指定数据
    else:
        shops = Shop.query.filter(Shop.source == classify).limit(30)

    return render_template('shop_list.html', shops = shops)


#404页面路由
@app.errorhandler(404)
def Four(error):
    print(error)
    return render_template('404.html',error = error),404

# 启动flask服务  默认地址为127.0.0.1:5000
app.run()