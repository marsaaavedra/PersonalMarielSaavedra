from flask import Flask, render_template, request,Response,jsonify,redirect,url_for
import database as dbase 
from product import Product
db=dbase.dbConnect()


app = Flask(__name__)
#Rutas de la aplicacion
@app.route('/')
def home():
    products=db["products"]
    productsReceived=products.find()    
    return render_template('index.html',products=productsReceived)


@app.route('/products',methods=['POST'])
def addProduct():
    products=db["products"]
    name=request.form['name']
    price=request.form['price']
    quantity=request.form['quantity']

    if name and price and quantity:
        product=Product(name,price,quantity)
        products.insert_one(product.toDBCollection())
        response=jsonify({
            "name":name,
            "price":price,
            "quantity":quantity
        })
        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/delete/<string:product_name>')
def deleteProduct(product_name):
    products=db["products"]
    result=products.delete_one({"name":product_name})
    if result.deleted_count>0:
        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products=db["products"]
    new_name=request.form['name']
    new_price=request.form['price']
    new_quantity=request.form['quantity']

    if new_name and new_price and new_quantity:
        result=products.update_one(
            {"name":product_name},
            {"$set":{
                "name":new_name,
                "price":new_price,
                "quantity":new_quantity 
            }}
        )
        if result.modified_count>0:
            response=jsonify({'message':'Producto actualizado correctamente'})     
            return redirect(url_for('home'))
        else:
            return notFound()
    else:
        return notFound()





@app.errorhandler(404)
def notFound(error=None):
    message={
        'status':404,
        'message':'No encontrado'+request.url
    }
    response=jsonify(message)
    response.status_code=404
    return response


if __name__ == '__main__':
    app.run(debug=True, port=4000)