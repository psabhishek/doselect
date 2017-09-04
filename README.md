# doselect

Step 1 : Signup -> Put Id and Password. It will return a key  @app.route('/signup', methods=['GET', 'POST'])

Step 2: Upload -> Put The key and the image path @app.route('/', methods=['GET', 'POST'])

Step 3: Show Single Image -> Put Key and the image name @app.route('/simgleImg', methods=['POST',"GET"])

Step 4: Show Gallery -> Put Key  @app.route('/gallery', methods=['POST',"GET"])

Step 5: Delete -> Put Key and the image name @app.route('/delete',methods = ['POST','GET'])
