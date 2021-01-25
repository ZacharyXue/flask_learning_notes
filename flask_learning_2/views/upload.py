from flask import Blueprint,request,render_template
from flask import current_app
import os
import json

upload_app = Blueprint("upload",__name__)

@upload_app.route('/',methods=['get','post'])
# xhr upload
def upload():
    if request.method == "POST":
        file_storages = request.files.getlist('file')
        message = {"result":"","error":"","file_pathlist":[]}
        for file_storage in file_storages:
            if request.content_length > 300 * 1000:
                message["result"] = "fail"
                message["error"] = " the file is too big"
                # 和使用form提交格式不同，使用xhr上传时要使用json，要发送相关信息
                return json.dumps(message)  # dumps将字符串转换为json字符串
            if file_storage.content_type not in \
                current_app.config['ALLOWED_UPLOAD_TYPE']:
                message["result"] = "fail"
                message["error"] = " the type of the file is not allowed"
                return json.dumps(message)
            # get_dir函数实现的是创建以日期为分类标准的文件存储地址
            # create_filename函数实现的创建文件名防止重复
            file_path = os.path.join(get_dir(),create_filename(file_storage.filename))
            try:
                file_storage.save(file_path)
            except Exception as e:
                message["result"] = "fail"
                message["error"] = str(e)
                return json.dumps(message)
            message['file_pathlist'].append(file_path[1:])
        message['result'] = 'success'
        return json.dumps(message)
    return render_template("upload/xhr_upload.html")
''' 
# form upload
def upload():
    if request.method == "POST":
        # upload only one file everytime
        file_storage = request.files.get('file')
        # 查询是否在可接受数据类型中
        if file_storage.content_type not in current_app.config['ALLOWED_UPLOAD_TYPE']:
            return "",403
        # 检查上传文件大小
        if request.content_length > 300 * 1000: # 300kb
            return "",403
        # 创建存储地址
        file_path = os.path.join(get_dir(),create_filename(file_storage.filename))
        file_storage.save(file_path)

        # upload files once
        # # 获得多个上传文件
        # file_storages = request.files.getlist('file')
        # # 遍历文件列表
        # for file_storage in file_storages:
        #     if file_storage.content_type not in \
        #         current_app.config['ALLOWED_UPLOAD_TYPE']:
        #         return '',403
        #     file_storage.save("./static/uploads/"+file_storage.filename) 
    return render_template('upload/form_upload.html')
'''

@upload_app.route('/ckeditor',methods=['post'])
def ckeditor_upload():
    if request.method == 'POST':
        file_storage = request.files.get('upload')
        message = {
            "uploaded":"0",
            "filename":"",
            "url":"",
            "error":{
                "message":""
            }
        }

        if request.content_length > 3000 * 1000:
            message['uploaded'] = "0"
            message['error']['message'] = " The file is too big"
            return json.dumps(message)
        if file_storage.content_type not in \
                current_app.config['ALLOWED_UPLOAD_TYPE']:
            message["uploaded"] = "0"
            message["error"]["message"] = " the type of the file is not allowed" 
            return json.dumps(message)
        
        file_path = os.path.join(get_dir(),create_filename(file_storage.filename))
        message['filename'] = file_storage.filename
        message['url'] = file_path[1:]  # 将相对路径转为绝对路径
        message['loaded'] = "1"
        return json.dumps(message)
        
def get_dir():
    '''
    store files by upload date
    '''
    from datetime import date

    base_dir = './static/uploads/'    
    d = date.today()
    path = os.path.join(base_dir,str(d.year),str(d.month))
    try:
        os.makedirs(path)
    except Exception as e:
        path = base_dir
        print(e)
    return path

def create_filename(filename):
    # uuid库使所有元素都有唯一的辨识信息
    import uuid
    # 保留后缀
    ext = os.path.splitext(filename)[1]
    filename2 = str(uuid.uuid4()) + ext
    return filename2