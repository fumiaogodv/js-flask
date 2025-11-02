from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# 获取当前 app.py 文件所在的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# 使用绝对路径拼接数据库文件地址
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "event.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ##################################################################
#  关键修改部分：添加一个中间件来处理 URL 前缀
# ##################################################################
class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        # 如果请求路径以指定的前缀开头，则移除前缀
        # 例如，将 /hello/wuziqi 修改为 /wuziqi
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            # 如果不匹配前缀，直接返回 404
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This URL does not belong to the app.".encode()]

# 将你的 Flask 应用包装在这个中间件中
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/hello')
# ##################################################################


# ------------------- 数据模型 -------------------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True,nullable=False)#不为空
    description = db.Column(db.String(120))
    date = db.Column(db.String(10))

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "date": self.date}

with app.app_context():
    db.create_all()

# ------------------- 页面路由 -------------------
@app.route("/")
def index():
    return render_template("display.html")

# ------------------- 获取事件列表 -------------------
@app.route("/api/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events])

# ------------------- 添加事件 -------------------
@app.route("/api/events/add", methods=["POST"])
def add_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "没有收到数据"}), 400

    title = data.get("title")
    description = data.get("description")
    date = data.get("date")

    if not title:
        return jsonify({"error": "缺少标题"}), 400

    new_event = Event(title=title, description=description, date=date)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({"message": "任务已插入数据库", "id": new_event.id})

@app.route("/api/events/find/<int:event_id>", methods=["GET"])
def find_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "未找到该ID对应的数据"}), 404

    # 假设 Event 模型有 id, title, description, date 等字段
    return jsonify({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date
    })

@app.route("/api/events/change",methods=["POST"])
def change_event():
    id_info=request.get_json()
    event_id=id_info.get('id')
    event=db.session.get(Event,event_id)
    if not event:
        return jsonify({"error": "未找到该ID对应的数据"}), 404

    # 假设 Event 模型有 id, title, description, date 等字段
    return jsonify({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date
    })
@app.route("/api/events/delect", methods=["POST"])
def delect_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "没有收到数据"}), 400

    delect_id = data.get("id")
    if not delect_id:
        return jsonify({"error": "没有提供 id"}), 400

    # 假设模型名为 Event
    event = db.session.get(Event, delect_id)  # ✅ SQLAlchemy 2.0 推荐写法
    if not event:
        return jsonify({"error": "该 id 不存在"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": f"已删除 id={delect_id}", "id": delect_id})


if __name__ == "__main__":
    app.run(debug=True)
