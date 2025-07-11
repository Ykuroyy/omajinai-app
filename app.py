from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
# SQLiteを使用してPostgreSQLの依存関係を回避
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///omajinai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)

# データベースモデル
class Omajinai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# デフォルトのおまじないデータ（30個）
default_omajinai = [
    {"text": "今日は新しい一日。昨日の嫌なことは水に流して、今日は笑顔で過ごしましょう！", "category": "気分転換"},
    {"text": "あなたは素晴らしい人です。他人の言葉に惑わされず、自分の価値を信じてください。", "category": "自信"},
    {"text": "深呼吸して、肩の力を抜いて。今日も頑張りすぎずに、ゆっくり進みましょう。", "category": "リラックス"},
    {"text": "雨の日も、晴れの日も、どちらも大切な一日。今日も感謝の気持ちで過ごしましょう。", "category": "感謝"},
    {"text": "小さな幸せを見つける心の余裕があれば、毎日が宝物になります。", "category": "幸せ"},
    {"text": "失敗しても大丈夫。それは成功への一歩です。今日も一歩ずつ進みましょう。", "category": "励まし"},
    {"text": "あなたの笑顔は、周りの人を幸せにします。今日も笑顔で過ごしましょう！", "category": "笑顔"},
    {"text": "嫌なことがあっても、それは一時的なもの。明日はきっと良いことがあります。", "category": "希望"},
    {"text": "自分を大切にすることは、周りの人を大切にすることと同じです。", "category": "自己愛"},
    {"text": "今日一日、無理をせずに、自分のペースで過ごしましょう。", "category": "ペース"},
    {"text": "星の光のように、あなたの内なる光が輝いています。それを信じて進みましょう。", "category": "内なる光"},
    {"text": "花が咲くように、あなたの夢も必ず花開きます。焦らずに、ゆっくり育ててください。", "category": "夢"},
    {"text": "風が運んでくる新しい香り。今日は新しい発見があるかもしれません。", "category": "発見"},
    {"text": "月の満ち欠けのように、人生にも良い時と悪い時があります。全ては必要な経験です。", "category": "人生"},
    {"text": "虹の七色のように、あなたの可能性は無限大です。色んなことに挑戦してみてください。", "category": "可能性"},
    {"text": "森の木々のように、根を深く張って、ゆっくりと大きく成長していきましょう。", "category": "成長"},
    {"text": "海の波のように、人生も浮き沈みがあります。でも、必ず新しい波が来ます。", "category": "波"},
    {"text": "朝日が昇るように、あなたの新しい一日も始まります。光に満ちた一日になりますように。", "category": "朝日"},
    {"text": "雪が溶けるように、心の氷も溶けて、温かい気持ちが戻ってきます。", "category": "心の温かさ"},
    {"text": "空の雲のように、心の重荷も流れていきます。軽やかな気持ちで過ごしましょう。", "category": "軽やかさ"},
    {"text": "蝶が羽ばたくように、あなたの心も自由に羽ばたいてください。", "category": "自由"},
    {"text": "夕日が沈むように、今日の疲れも一緒に流れていきます。", "category": "休息"},
    {"text": "宝石のように、あなたの心も美しく輝いています。", "category": "美しさ"},
    {"text": "音楽のように、人生にもリズムがあります。そのリズムに合わせて踊りましょう。", "category": "リズム"},
    {"text": "魔法のように、あなたの言葉には人を幸せにする力があります。", "category": "言葉の力"},
    {"text": "星座のように、あなたの道筋は既に決まっています。迷わずに進みましょう。", "category": "道筋"},
    {"text": "春の芽吹きのように、新しい始まりの時です。", "category": "新しい始まり"},
    {"text": "秋の紅葉のように、変化も美しいものです。", "category": "変化"},
    {"text": "冬の静寂のように、時には静かに自分と向き合うことも大切です。", "category": "内省"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/omajinai')
def omajinai():
    omajinai_list = Omajinai.query.all()
    if not omajinai_list:
        for item in default_omajinai:
            new_omajinai = Omajinai(text=item["text"], category=item["category"])
            db.session.add(new_omajinai)
        db.session.commit()
        omajinai_list = Omajinai.query.all()
    today_omajinai = random.choice(omajinai_list)
    return render_template('omajinai.html', omajinai=today_omajinai)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 