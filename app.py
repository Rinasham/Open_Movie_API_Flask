from flask import Flask, render_template, request, redirect
import requests
import codecs
import settings

key = settings.AP
print(key)


app = Flask(__name__)
history_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie')
def search_title():
  movie_request = request.args.get('movie')

  # send a request to API server
  res = requests.get(f'http://www.omdbapi.com/?t={movie_request}&apikey={key}').json()
  status = res['Response']
  if status == 'False' or movie_request == 'None':
    return render_template('fail.html')
  else:
    rating = float(res['Ratings'][0]['Value'][0:3])
    star_rating = round(rating/2)

    dict = {
      'title' : res['Title'],
      'img_url' : res['Poster'],
      'year' : res['Year'],
      'rating' : rating,
      'star-rating' : star_rating,
    }

    # write into 'history.txt'
    if not res['Title'] in history_list:
      # open 'history.txt'
      target_file = codecs.open('history.txt', "a", "utf_8")
      history_list.append(res['Title'])
      try:
        target_file.write(f"\n{res['Title']}")
      except:
        # error handling
        print("could not write into history.txt")
      # close 'history.txt'
      target_file.close()
  # respond to the client
    return render_template('detail.html', dict = dict)

@app.route('/search')
def search():
  list_request = request.args.get('movie_search')
  res = requests.get(f'http://www.omdbapi.com/?s={list_request}&apikey={key}').json()
  title_list = []

  if res['Response'] == 'True':
    for movie in res['Search']:
      title_list.append(movie['Title'])

    if len(title_list) > 1:
      return render_template('search_result.html', list = title_list)
    else:
      return redirect(f'/movie?movie={title_list[0]}')


  else:
    return render_template('fail.html')


@app.route('/history')
def history():
  file=codecs.open("history.txt", "r", "utf-8")
  lines=file.readlines()
  file.close()
  return render_template('history.html', lines=lines)


if __name__ == '__main__':
    app.run(debug=True)