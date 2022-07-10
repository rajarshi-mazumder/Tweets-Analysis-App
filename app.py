
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from forms import UserForm, TwitterSearchForm
import twitter_bot_python as bot
import twitter_bot_test as bot2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zfldepccsydywe:199084877f6571c67b03c4b5ba0aa0fd6dc3a4db7e46bc54645bdcc01d9657ad@ec2-52-22-136-117.compute-1.amazonaws.com:5432/db00s6gbl9viqd'
app.config['SECRET_KEY'] = "e07e5ecdb25b94b71947500f166ce38e"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name


# @app.route("/", methods=['GET', 'POST'])
# @app.route("/home", methods=['GET', 'POST'])
# def index():
#     form = UserForm()
#     anime_list = ["Attack on Titan", "Steins;Gate", "Fate Series"]
#     if form.validate_on_submit():
#         existing_user = Users.query.filter_by(email=form.email_id.data).first()
#         if existing_user is None:

#             user = Users(name=form.username.data, email=form.email_id.data)
#             try:
#                 db.session.add(user)
#                 db.session.commit()
#                 website_users = Users.query.order_by(Users.date_added)
#                 flash("Subscribed! I'll let you know if I make any updates! :)")
#                 # return render_template('test.html', form=form, website_users=website_users)
#                 return render_template('index.html', anime_list=anime_list, form=form, website_users=website_users)
#             except:
#                 flash("Sorry, there was an error! T__T")
#                 website_users = Users.query.order_by(Users.date_added)
#                 return render_template('test.html', form=form, website_users=website_users)
#                 return render_template('index.html', anime_list=anime_list, form=form)
#         else:
#             flash("User already exists in database!")
#             website_users = Users.query.order_by(Users.date_added)
#             return render_template('test.html', form=form, website_users=website_users)

#     website_users = Users.query.order_by(Users.date_added)
#     return render_template('index.html', anime_list=anime_list, form=form, website_users=website_users)


@app.route('/analyse_tweets', methods=['GET', 'POST'])
def analyse_tweets():
    not_well_classified = False
    form = TwitterSearchForm()
    if form.validate_on_submit():
        username = form.username.data
        number_of_tweets = form.number_of_tweets.data
        # x_coord, y_coord = bot.plot_graph(username, number_of_tweets)
        # x_coord, y_coord, tweets_dict = bot2.plot_graph(
        #     username, number_of_tweets)

        try:
            x_coord, y_coord, tweets_dict = bot2.tweets_analysis(
                username, number_of_tweets)
            data = {}
            for i in range(7):
                data[x_coord[i]] = y_coord[i]

            if y_coord[1] < 5:
                not_well_classified = True
            # return render_template('charts.html', data=data)
            return render_template('result.html', username=username, x_coord=x_coord, y_coord=y_coord, data=data, tweets_dict=tweets_dict, number_of_tweets=number_of_tweets, not_well_classified=not_well_classified)
        except:
            flash(
                "Couldn't get data for the username you entered <html>&#128557;</html>  Are you sure the account exists and is public?")
            return render_template('analyse_tweets.html', form=form)
    return render_template('analyse_tweets.html', form=form)

# Fav users start


@app.route('/analyse_tweets_for/<string:username>', methods=['GET', 'POST'])
def analyse_tweets_for(username):
    not_well_classified = False
    form = TwitterSearchForm()

    try:
        x_coord, y_coord, tweets_dict = bot2.tweets_analysis(
            username, 200)
        data = {}
        for i in range(7):
            data[x_coord[i]] = y_coord[i]
        # return render_template('charts.html', data=data)

        if y_coord[1] < 5:
            not_well_classified = True
        print(not_well_classified)
        return render_template('result.html', username=username, x_coord=x_coord, y_coord=y_coord, data=data, tweets_dict=tweets_dict, number_of_tweets=200, not_well_classified=not_well_classified)
    except:
        flash(
            "Couldn't get data for the username you entered <html>&#128557;</html>  Maybe this account isn't public anymore!")
        return render_template('analyse_tweets.html', form=form)
    return render_template('analyse_tweets.html', form=form)


# Fav users end

@app.route('/charts', methods=['GET', 'POST'])
def display_charts():

    data = {}
    x_coord, y_coord = bot.plot_graph('fabrizioromano', 200)
    # for i in range(6):
    #     data[topic_names[i]] = topic_mentions[i]
    for i in range(7):
        data[x_coord[i]] = y_coord[i]

    # data = {'topic': 'mentions', 'ronaldo': 32, 'messi': 25,
    #         'cristiano': 21, 'league': 9, 'madrid': 6, 'united': 5}

    return render_template('charts.html', data=data)
    # return render_template('charts.html', arr=arr)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def index():
    form = UserForm()

    # return render_template('test.html', form=form, website_users=website_users)

    #
    if form.validate_on_submit():
        existing_user = Users.query.filter_by(email=form.email_id.data).first()
        if existing_user is None:

            user = Users(name=form.username.data, email=form.email_id.data)
            try:
                db.session.add(user)
                db.session.commit()
                website_users = Users.query.order_by(Users.date_added)
                flash("Subscribed! I'll let you know if I make any updates! :)")
                return render_template('test.html', form=form, website_users=website_users)
                # return render_template('index.html', anime_list=anime_list, form=form, website_users=website_users)
            except:
                flash("Sorry, there was an error! T__T")
                website_users = Users.query.order_by(Users.date_added)
                return render_template('test.html', form=form, website_users=website_users)
                return render_template('index.html', anime_list=anime_list, form=form)
        else:
            flash("User already exists in database!")
            website_users = Users.query.order_by(Users.date_added)
            return render_template('test.html', form=form, website_users=website_users)

    website_users = Users.query.order_by(Users.date_added)
    return render_template('test.html', form=form, website_users=website_users)
    # return render_template('index.html', anime_list=anime_list, form=form, website_users=website_users)
    #


@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/termsandconditions')
def termsandconditions():
    return render_template('tandc.html')


@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')


@app.route('/test2')
def test2():
    return render_template('test2.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
