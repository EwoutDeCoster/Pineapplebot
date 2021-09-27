from flask import Flask, make_response, jsonify, request
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('/root/Pineapple/cogs/main.sqlite')
cursor = db.cursor()


def fetch_db(guild_id):
    cursor.execute(
        f"SELECT lvl, exp, user FROM leveling WHERE guild_id = {guild_id} ORDER BY lvl DESC, exp DESC LIMIT 5")
    result = cursor.fetchall()
    return result


@app.route('/')
def home():
    return "<h1>Testje dabei<h1>"


@app.route('/api/leaderboard/<guild_id>', methods=['GET'])
def api_each_book(guild_id):
    if request.method == "GET":
        guildobj = fetch_db(guild_id)
        if guildobj:
            return make_response(jsonify(guildobj), 200)
        else:
            return make_response(jsonify(guildobj), 404)


if __name__ == '__main__':
    app.run(debug=True)
