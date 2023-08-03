from flask import Flask, Response
import requests as req
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

end = [0, 399, 799, 999, 1199, 1399, 1599, 1799, 1999, 2199, 2399, 2599, 2999, 3000]

Card_bg = [
    '858a93',  # Unrated
    '725541',  # C / C+
    '394a7f',  # B / B+
    'f7b551',  # A / A+
    '60db79',  # S / S+
    '53ace0',  # SS / SS+
    'fc4964'  # SSS / SSS+
]

Mini_bg = ['#818996', '#725039', '#2c4182', '#ffa515', '#46db66', '#30a1e5', '#ff143b', '']

Tier_Color = ['#818996', '#725039', '#2c4182', '#ffa515', '#46db66', '#30a1e5', '#ff143b', '']

Color_Num = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6]
Tier = ['Unrated', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S', 'S+', 'SS', 'SS+', 'SSS', 'SSS+', 'X']
Tier_mini = ['?', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S', 'S+', 'SS', 'SS+', 'SSS', 'SSS+', 'X']

Max_Len = 13


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'max-age=1800'
    return response


@app.route("/v1/<string:name>", methods=['GET'])
def Create_V1_Badge(name):
    URL = f'https://solved.ac/api/v3/user/show?handle={name}'
    Tier_X_decorate = '''<rect width='10' height='260' transform='rotate(-45)' x='50' y='40'></rect>
  <rect width='10' height='260' transform='rotate(45)' x='190' y='-210'></rect>'''

    try:
        get = req.get(URL).json()
        if len(name) > Max_Len: name = name[:13] + '...'
        data = [get['arenaTier'], get['arenaRating'], get['arenaMaxRating'], get['arenaCompetedRoundCount'],
                get['arenaMaxTier']]

        MyTier = data[0]
        Rating = data[1]
        percent = int((Rating / end[MyTier] if end[MyTier] != 0 else 1) * 100)
        if percent >= 100: percent = 100
        if MyTier != 13: Tier_X_decorate = ''

        SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="350" height="170">
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Jost');
    .card-bg {{
        fill:{fill}
    }}
    .Max-Tier {{fill: white; font-family: 'Jost', sans-serif;}}
    .Tier {{fill: white; font-size:1.6em; font-family: 'Jost', sans-serif;}}

    .sf {{font-size:0.9em; font-family: 'Jost', sans-serif;}}
    .bf {{font-size:1.3em; font-family: 'Jost', sans-serif;}}

    .bar-frame {{
      fill: white; animation-name: move;
      animation-duration: 2s;
      animation-delay: 1.5s;
      animation-iteration-count: 1;
    }}

    @keyframes move {{
      from {{
        width:0
      }}
      to {{
        width: 300
      }}
    }}
  </style>


  <rect width="350" height="170" class="card-bg" rx="7" ry="7"/>

  {TierX}

  <text id="User" x="20" y="45" font-weight="bold" class="bf" fill="white">{username}</text>
  <text id="Round" x="20" y="80" class="sf" fill="white">Total Round {Total}</text>
  <text id="Max" x="20" y="100" class="sf" fill="white">Max Tier <tspan class="Max-Tier"> {MaxTier} {MaxRating}</tspan></text>
  <text id="Tier" class="Tier" x="310" y="50" text-anchor="end" font-weight="bold">{CTier}</text>

  <text id='Rating' x='330' y='155' fill="white" font-size="11" text-anchor='end' font-family='Jost'>{rating} / {end}</text>
  <text id='percent' x='310' y='140' fill='white' font-size='11' font-family='Jost'>{per}%</text>

  <rect width="290" height="10" x="15.5" y="130" fill="gray" rx="3.8"/>
  <rect width="{bar}" height="10" x="15.5" y="130" class="bar-frame" rx="3.8"/>
</svg>'''.format(username=name,
                 Total=data[3],
                 MaxTier=Tier[data[4]],
                 MaxRating=data[2],
                 CTier=Tier[MyTier],
                 per=percent,
                 fill='#' + Card_bg[Color_Num[MyTier]],
                 bar=percent / 100 * 290,
                 rating=Rating,
                 end=end[MyTier],
                 TierX=Tier_X_decorate)
    except:
        return Response('error', 404)
    return Response(SVG, mimetype='image/svg+xml'), 200


@app.route("/v1/mini/<string:name>", methods=['GET'])
def Create_V1_Mini_Badge(name):
    URL = f'https://solved.ac/api/v3/user/show?handle={name}'

    Tier_X_decorate = '''<rect width="10" height="20" x="70" y="0" rx="3" ry="3" fill='red'/>
        <rect width="10" height="20" x="105" y="0" fill='red'/>'''

    try:
        get = req.get(URL).json()

        data = get['arenaTier']

        if data != 13: Tier_X_decorate = ''

        SVG = '''<svg height="20" width="110"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xml:space="preserve">
            <style>
              @import url('https://fonts.googleapis.com/css2?family=Jost');
              text {{font-family: 'Jost'}}
            </style>

            <defs>
                <clipPath id="round-corner">
                    <rect x="0" y="0" width="110" height="20" rx="3" ry="3"/>
                </clipPath>
            </defs>
            <rect width="40" height="20" x="70" y="0" rx="3" ry="3" fill='{fill}'/>
            {Tier_X_decorate}
            <rect width="75" height="20" clip-path="url(#round-corner)"  fill='#555555'/>
            <text text-anchor="middle" alignment-baseline="middle" dominant-baseline="middle" transform="translate(37.5, 11)" fill='white' font-size='0.7em'>AC Arena</text>
            <text font-size='0.78em' fill='white' text-anchor="middle" alignment-baseline="middle" dominant-baseline="middle" transform="translate(92, 11)">{Tier}</text>
        </svg>'''.format(fill=Tier_Color[Color_Num[data]],
                         Tier_X_decorate=Tier_X_decorate,
                         Tier=Tier_mini[data])
    except:
        return Response('Error', 404)
    return Response(SVG, mimetype='image/svg+xml'), 200